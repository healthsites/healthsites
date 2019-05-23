from api.utils import validate_osm_data, convert_to_osm_tag, update_osm_node
from core.settings.utils import ABS_PATH

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import Http404, HttpResponseBadRequest
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


class GetDetailFacility(FacilitiesBaseAPI):
    """
    get:
    Returns a facility detail.

    put:
    Update a facility.
    """

    def get(self, request, osm_type, osm_id):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        if osm_type == 'node':
            self.JSONSerializer = LocalityOSMNodeSerializer
            self.GEOJSONSerializer = LocalityOSMNodeGeoSerializer
            try:

                facility = LocalityOSMNode.objects.get(osm_id=osm_id)
                return Response(self.serialize(facility))
            except LocalityOSMNode.DoesNotExist:
                raise Http404()
        elif osm_type == 'way':
            self.JSONSerializer = LocalityOSMWaySerializer
            self.GEOJSONSerializer = LocalityOSMWayGeoSerializer
            try:

                facility = LocalityOSMWay.objects.get(osm_id=osm_id)
                return Response(self.serialize(facility))
            except LocalityOSMNode.DoesNotExist:
                raise Http404()
        else:
            return HttpResponseBadRequest('%s is not recognized as osm type' % osm_type)

    def put(self, request, osm_type, osm_id):
        data = request.data
        # Now, we post the data directly to OSM.
        try:
            if osm_type == 'node':
                data['id'] = osm_id

                # Validate data
                is_valid, message = validate_osm_data(data)
                if not is_valid:
                    return HttpResponseBadRequest(message)

                # Map Healthsites tags to OSM tags
                mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
                data['tag'] = convert_to_osm_tag(
                    mapping_file_path, data['tag'], 'node')

                # Push data to OSM
                user = request.user
                response = update_osm_node(user, data)

                return Response(response)

        except Exception as e:
            return HttpResponseBadRequest('%s' % e)
