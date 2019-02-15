__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.api_views.v2.schema import (
    ApiSchemaBase,
    ApiSchemaBaseWithoutApiKey,
    Parameters
)
from api.api_views.v2.utilities import BadRequestError
from api.serializer.locality_post import LocalityPostSerializer
from api.api_views.v2.facilities.base_api import (
    PaginationAPI
)
from localities.models import Country, Locality
from localities_osm.models.locality import LocalityOSMView
from localities.utils import parse_bbox


class CountScheme(ApiSchemaBaseWithoutApiKey):
    schemas = [
        Parameters.country, Parameters.extent, Parameters.output
    ]


class ApiSchema(ApiSchemaBase):
    schemas = [
        Parameters.page, Parameters.country, Parameters.extent, Parameters.output
    ]


class GetFacilitiesUtilities(object):
    """
    Parent class that hold filtering method of healthsites
    """

    def get_healthsites(self, request):

        # check extent data
        extent = request.GET.get('extent', None)
        queryset = LocalityOSMView.objects.all()
        if extent:
            try:
                polygon = parse_bbox(request.GET.get('extent'))
            except (ValueError, IndexError):
                raise BadRequestError('extent is incorrect format')
            queryset = queryset.in_polygon(polygon)

        # check by country
        country = request.GET.get('country', None)
        if country == 'World':
            country = None
        if country:
            # getting country's polygon
            try:
                country = Country.objects.get(
                    name__iexact=country)
                polygons = country.polygon_geometry
                queryset = queryset.in_polygon(polygons)
            except Country.DoesNotExist:
                raise BadRequestError('%s is not found or not a country.' % country)
        return queryset


class GetFacilities(PaginationAPI, GetFacilitiesUtilities):
    """
    get:
    Returns a list of facilities with some filtering parameters.

    post:
    Create new facility.
    """
    filter_backends = (ApiSchema,)

    def get_serializer(self):
        return LocalityPostSerializer()

    def get(self, request):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        queryset = self.get_query_by_page(self.get_healthsites(request))
        return Response(self.serialize(queryset, many=True))

    def post(self, request):
        data = request.data
        facility = Locality()
        try:
            data = self.parse_data(data)
            facility.update_data(data, request.user)
            return Response(self.serialize(facility), status=status.HTTP_201_CREATED)
        except KeyError as e:
            return HttpResponseBadRequest('%s is required' % e)
        except ValueError as e:
            return HttpResponseBadRequest('%s' % e)
        except Exception as e:
            return HttpResponseBadRequest('%s' % e)


class GetFacilitiesCount(APIView, GetFacilitiesUtilities):
    """
    get:
    Returns count of facilities with some filtering parameters.
    """
    filter_backends = (CountScheme,)

    def get(self, request):
        try:
            return Response(self.get_healthsites(request).count())
        except BadRequestError as e:
            return HttpResponseBadRequest('%s' % e)
