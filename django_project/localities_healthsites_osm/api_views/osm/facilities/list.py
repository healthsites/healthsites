__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.schema import (
    ApiSchemaBase,
    Parameters
)
from api.api_views.v2.facilities.base_api import (
    PaginationAPI
)
from localities_osm.models.locality import LocalityOSMView
from localities.utils import parse_bbox
from localities_healthsites_osm.serializer.locality import (
    LocalityHealthsitesOSMSerializer,
    LocalityHealthsitesOSMGeoSerializer
)


class ApiSchema(ApiSchemaBase):
    schemas = [
        Parameters.page, Parameters.extent,
        Parameters.output
    ]


class GetFacilities(PaginationAPI):
    """
    get:
    Returns a list of facilities with some filtering parameters.
    """
    filter_backends = (ApiSchema,)
    JSONSerializer = LocalityHealthsitesOSMSerializer
    GEOJSONSerializer = LocalityHealthsitesOSMGeoSerializer

    def get(self, request):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        # check extent data
        extent = request.GET.get('extent', None)
        queryset = LocalityOSMView.objects.all()
        if extent:
            try:
                polygon = parse_bbox(request.GET.get('extent'))
            except (ValueError, IndexError):
                return HttpResponseBadRequest('extent is incorrect format')
            queryset = queryset.in_polygon(polygon)
        queryset = self.get_query_by_page(queryset)
        return Response(self.serialize(queryset, many=True))
