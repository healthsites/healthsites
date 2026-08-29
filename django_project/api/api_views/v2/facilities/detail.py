__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import copy
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response

from api.api_views.v2.base_api import BaseAPIWithAuthAndApiKey
from api.api_views.v2.facilities.base_api import FacilitiesBaseAPI
from api.api_views.v2.schema import FacilityRequestSchema, Parameters
from api.utilities.pending import (
    create_pending_update, validate_pending_update,
    create_pending_review, update_pending_review, delete_pending_review,
    get_pending_review)
from api.utils import (
    validate_osm_data, convert_to_osm_tag,
    update_osm_node, update_osm_way, verify_user)
from core.settings.utils import ABS_PATH
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
from localities_osm_extension.models.extension import LocalityOSMExtension

_OSM_TYPE_PARAM = OpenApiParameter(
    'osm_type', str, OpenApiParameter.PATH,
    description='OSM element type.',
    enum=['node', 'way'],
)
_OSM_ID_PARAM = OpenApiParameter(
    'osm_id', int, OpenApiParameter.PATH,
    description='OSM element ID.',
)
_UUID_PARAM = OpenApiParameter(
    'uuid', str, OpenApiParameter.PATH,
    description='Facility UUID.',
)


class GetDetailFacility(FacilitiesBaseAPI):
    """Facility detail and update endpoint, addressed by OSM type and ID."""

    def getLocalityOsm(self, osm_type, osm_id):
        """ Get locality osm """

        if osm_type == 'node':
            return LocalityOSMNode.objects.get(osm_id=osm_id)
        elif osm_type == 'way':
            return LocalityOSMWay.objects.get(osm_id=osm_id)
        else:
            return None

    @extend_schema(
        summary='Get facility detail',
        description='Returns the full detail of a single facility by OSM type and ID.',
        parameters=[_OSM_TYPE_PARAM, _OSM_ID_PARAM, Parameters.output],
    )
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
            return Response(
                self.serialize(self.getLocalityOsm(osm_type, osm_id)))
        except (LocalityOSMNode.DoesNotExist, LocalityOSMWay.DoesNotExist):
            raise Http404()

    @extend_schema(
        summary='Update facility',
        description='Update an existing facility node or way in OpenStreetMap.',
        parameters=[_OSM_TYPE_PARAM, _OSM_ID_PARAM],
        request=FacilityRequestSchema.create_request,
        examples=FacilityRequestSchema.create_examples,
    )
    def post(self, request, osm_type, osm_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        data = copy.deepcopy(request.data)
        user = request.user
        if user.username in settings.TEST_USERS:
            raise Exception(
                'Update osm : {}'.format(
                    json.dumps(
                        {
                            'payload': data,
                            'user': user.username,
                            'osm_id': osm_id,
                            'osm_type': osm_type
                        })
                )
            )

        # delete uuid, because it is not editable
        try:
            del data['tag']['uuid']
        except KeyError:
            pass

        # Now, we post the data directly to OSM.
        try:
            if osm_type == 'node':
                osm_function = update_osm_node
            elif osm_type == 'way':
                osm_function = update_osm_way
            else:
                # For now, we only support Node
                return HttpResponseBadRequest(
                    '%s is not supported as osm type' % osm_type)
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
                mapping_file_path, data['tag'], osm_type)

            # Push data to OSM
            response = osm_function(user, data)

            create_pending_update(
                osm_type,
                response['id'],
                data['tag']['name'],
                user,
                response['version']
            )
            if request.GET.get('review', None):
                delete_pending_review(request.GET.get('review', None))
            return Response(response)

        except KeyError as e:
            return HttpResponseBadRequest('%s is needed' % e)
        except (LocalityOSMNode.DoesNotExist, LocalityOSMNode.DoesNotExist):
            raise Http404(
                "Facility not found. Please check your OSM ID and OSM TYPE."
            )
        except Exception as e:
            if not request.GET.get('review', None):
                if user != request.user:
                    create_pending_review(user, request.data, '%s' % e)
            else:
                try:
                    update_pending_review(request.GET.get(
                        'review', None), request.data, '%s' % e)
                except Exception as e:
                    return HttpResponseBadRequest('%s' % e)
            output = {
                'error': '%s' % e,
                'payload': request.data,
            }
            return HttpResponseBadRequest('%s' % json.dumps(output))


class GetDetailFacilityV3(GetDetailFacility, BaseAPIWithAuthAndApiKey):
    """Authenticated facility detail and update endpoint (API v3)."""

    api_label = {
        'POST': 'update'
    }


class GetDetailFacilityByUUID(GetDetailFacility):
    """Facility detail and update endpoint, addressed by UUID."""

    def get_facility_by_uuid(self, uuid):
        extension = LocalityOSMExtension.get_extension_by_uuid(uuid)
        if not extension:
            raise Http404('not found')
        return extension.osm_type, extension.osm_id

    @extend_schema(
        summary='Get facility detail by UUID',
        description='Returns the full detail of a single facility by its UUID.',
        parameters=[_UUID_PARAM, Parameters.output],
    )
    def get(self, request, uuid):
        osm_type, osm_id = self.get_facility_by_uuid(uuid)
        return super(GetDetailFacilityByUUID, self).get(
            request, osm_type, osm_id)

    @extend_schema(
        summary='Update facility by UUID',
        description='Update an existing facility in OpenStreetMap by its UUID.',
        parameters=[_UUID_PARAM],
    )
    def post(self, request, uuid):
        osm_type, osm_id = self.get_facility_by_uuid(uuid)
        return super(GetDetailFacilityByUUID, self).post(
            request, osm_type, osm_id)
