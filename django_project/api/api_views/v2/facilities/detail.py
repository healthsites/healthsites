__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import copy
import json
from core.settings.utils import ABS_PATH

from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api.api_views.v2.facilities.base_api import (
    FacilitiesBaseAPI
)
from localities_osm.models.locality import (
    LocalityOSMNode,
    LocalityOSMWay
)
from localities_osm.serializer.locality_osm import (
    LocalityOSMNodeSerializer,
    LocalityOSMNodeGeoSerializer,
    LocalityOSMWaySerializer,
    LocalityOSMWayGeoSerializer
)
from api.utilities.pending import (
    create_pending_update, validate_pending_update,
    create_pending_review, update_pending_review, delete_pending_review,
    get_pending_review)
from api.utils import (
    validate_osm_data, convert_to_osm_tag, update_osm_node, verify_user)


class GetDetailFacility(FacilitiesBaseAPI):
    """
    get:
    Returns a facility detail.

    put:
    Update a facility.
    """

    def getLocalityOsm(self, osm_type, osm_id):
        """"""

        if osm_type == 'node':
            return LocalityOSMNode.objects.get(osm_id=osm_id)
        elif osm_type == 'way':
            return LocalityOSMWay.objects.get(osm_id=osm_id)
        else:
            return None

    def get(self, request, osm_type, osm_id):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        pending = validate_pending_update(osm_type, osm_id)
        if pending:
            return HttpResponseBadRequest('Still in pending')

        if osm_type == 'node':
            self.JSONSerializer = LocalityOSMNodeSerializer
            self.GEOJSONSerializer = LocalityOSMNodeGeoSerializer
        elif osm_type == 'way':
            self.JSONSerializer = LocalityOSMWaySerializer
            self.GEOJSONSerializer = LocalityOSMWayGeoSerializer
        else:
            return HttpResponseBadRequest(
                '%s is not recognized as osm type' % osm_type)

        try:
            return Response(self.serialize(self.getLocalityOsm(osm_type, osm_id)))
        except (LocalityOSMNode.DoesNotExist, LocalityOSMNode.DoesNotExist):
            raise Http404()

    def post(self, request, osm_type, osm_id):
        data = copy.deepcopy(request.data)
        user = request.user
        # Now, we post the data directly to OSM.
        try:
            if osm_type == 'node':
                locality = self.getLocalityOsm(osm_type, osm_id)
                data['id'] = osm_id
                data['type'] = osm_type
                data['version'] = locality.changeset_version

                # Verify data uploader and owner/collector if the API is being
                # used for uploading data from other osm user.
                if request.user.is_staff and request.GET.get('review', None):
                    data['osm_user'] = get_pending_review(
                        request.GET.get('review')).uploader.username

                if data.get('osm_user'):
                    is_valid, message = verify_user(user, data['osm_user'])
                    if not is_valid:
                        return HttpResponseForbidden(message)
                    else:
                        try:
                            user = get_object_or_404(
                                User, username=data['osm_user'])
                        except Http404:
                            message = 'User %s is not exist.' % data[
                                'osm_user']
                            return HttpResponseForbidden(message)

                # Validate data
                validate_osm_data(data, duplication_check=False)

                # Map Healthsites tags to OSM tags
                mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
                data['tag'] = convert_to_osm_tag(
                    mapping_file_path, data['tag'], 'node')

                # Push data to OSM
                response = update_osm_node(user, data)

                create_pending_update(
                    'node',
                    response['id'],
                    data['tag']['name'],
                    user,
                    response['version']
                )
                if request.GET.get('review', None):
                    delete_pending_review(request.GET.get('review', None))
                return Response(response)
            else:
                # For now, we only support Node
                return HttpResponseBadRequest(
                    '%s is not supported as osm type' % osm_type)

        except KeyError as e:
            return HttpResponseBadRequest('%s is needed' % e)
        except Exception as e:
            if not request.GET.get('review', None):
                if user != request.user:
                    create_pending_review(user, request.data, '%s' % e)
            else:
                try:
                    update_pending_review(request.GET.get('review', None), request.data, '%s' % e)
                except Exception as e:
                    return HttpResponseBadRequest('%s' % e)
            output = {
                'error': '%s' % e,
                'payload': request.data,
            }
            return HttpResponseBadRequest('%s' % json.dumps(output))
        except (LocalityOSMNode.DoesNotExist, LocalityOSMNode.DoesNotExist):
            raise Http404()
