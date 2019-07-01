__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from api.api_views.v2.schema import (
    ApiSchemaBase,
    ApiSchemaBaseWithoutApiKey,
    Parameters
)
from api.api_views.v2.utilities import BadRequestError
from api.api_views.v2.pagination import (
    PaginationAPI, LessThanOneException, NotANumberException
)
from api.api_views.v2.facilities.base_api import FacilitiesBaseAPIWithAuth
from api.utils import validate_osm_data, convert_to_osm_tag, create_osm_node
from api.utilities.statistic import get_statistic_with_cache
from core.settings.utils import ABS_PATH
from localities.models import Country
from api.utilities.pending import create_pending
from localities_osm.queries import filter_locality
from localities_osm.utilities import split_osm_and_extension_attr
from localities_osm_extension.utils import save_extensions


class FilterFacilitiesScheme(ApiSchemaBaseWithoutApiKey):
    schemas = [
        Parameters.country, Parameters.extent, Parameters.output
    ]


class ApiSchema(ApiSchemaBase):
    schemas = [Parameters.page] + FilterFacilitiesScheme.schemas


class GetFacilitiesBaseAPI(object):
    """
    Parent class that hold filtering method of healthsites
    """

    def get_country(self, country):
        """ This function is for get country object from request
        """
        # check by country
        if country == 'World':
            country = None
        if country:
            # getting country's polygon
            country = Country.objects.get(
                name__iexact=country)
        return country

    def get_healthsites(self, request):
        extent = request.GET.get('extent', None)
        country = request.GET.get('country', None)

        # check extent data
        try:
            queryset = filter_locality(
                extent=extent, country=country)
        except Exception as e:
            raise BadRequestError('%s' % e)
        return queryset


class GetFacilities(PaginationAPI, FacilitiesBaseAPIWithAuth, GetFacilitiesBaseAPI):
    """
    get:
    Returns a list of facilities with some filtering parameters.

    post:
    Create new facility.
    """
    filter_backends = (ApiSchema,)

    def get(self, request):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        try:
            queryset = self.get_query_by_page(self.get_healthsites(request))
        except (LessThanOneException, NotANumberException) as e:
            return HttpResponseBadRequest('%s' % e)

        return Response(self.serialize(queryset, many=True))

    def post(self, request):
        data = request.data
        # Now, we post the data directly to OSM.
        try:
            # Validate data
            osm_attr, locality_attr = split_osm_and_extension_attr(
                data['tag'])
            data['tag'] = osm_attr

            is_valid, message = validate_osm_data(data)
            if not is_valid:
                return HttpResponseBadRequest(message)

            # Map Healthsites tags to OSM tags
            mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
            data['tag'] = convert_to_osm_tag(
                mapping_file_path, data['tag'], 'node')

            # Push data to OSM
            user = request.user
            response = create_osm_node(user, data)

            # create pending index
            create_pending('node', response['id'], data['tag']['name'], user, response['version'])

            save_extensions('node', response['id'], locality_attr)
            return Response(response)

        except Exception as e:
            return HttpResponseBadRequest('%s' % e)


class GetFacilitiesCount(APIView, GetFacilitiesBaseAPI):
    """
    get:
    Returns count of facilities with some filtering parameters.
    """
    filter_backends = (FilterFacilitiesScheme,)

    def get(self, request):
        try:
            country = request.GET.get('country', None)
            extent = request.GET.get('extent', None)

            # get cache data
            output = get_statistic_with_cache(extent, country)
            return Response(output['localities'])
        except Exception as e:
            return HttpResponseBadRequest('%s' % e)


class GetFacilitiesStatistic(APIView, GetFacilitiesBaseAPI):
    """
    get:
    Returns statistic of facilities with some filtering parameters.
    """
    filter_backends = (FilterFacilitiesScheme,)

    def get(self, request):
        try:
            country = request.GET.get('country', None)
            extent = request.GET.get('extent', None)

            # get cache data
            output = get_statistic_with_cache(extent, country)
            if country:
                country = self.get_country(country)
                output['geometry'] = country.polygon_geometry.geojson
            return Response(output)
        except Exception as e:
            return HttpResponseBadRequest('%s' % e)
