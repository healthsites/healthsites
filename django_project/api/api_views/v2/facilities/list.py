__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from datetime import datetime
from django.http.response import HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from api.api_views.v2.schema import (
    ApiSchemaBase,
    Parameters
)
from api.serializer.locality_post import LocalityPostSerializer
from api.api_views.v2.facilities.base_api import (
    PaginationAPI
)
from localities.models import Locality
from localities.utils import get_heathsites_master, parse_bbox


class ApiSchema(ApiSchemaBase):
    schemas = [
        Parameters.page, Parameters.extent,
        Parameters.timestamp_from, Parameters.timestamp_to,
        Parameters.output
    ]


class GetFacilities(PaginationAPI):
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

        # check extent data
        extent = request.GET.get('extent', None)
        queryset = get_heathsites_master()
        if extent:
            try:
                polygon = parse_bbox(request.GET.get('extent'))
            except (ValueError, IndexError):
                return HttpResponseBadRequest('extent is incorrect format')
            queryset = queryset.in_polygon(polygon)

        # check by timestamp data
        timestamp_from = request.GET.get('from', None)
        if timestamp_from:
            try:
                queryset = queryset.from_datetime(
                    datetime.fromtimestamp(int(timestamp_from))
                )
            except TypeError:
                return HttpResponseBadRequest('From needs to be in integer')
        timestamp_to = request.GET.get('to', None)
        if timestamp_to:
            try:
                queryset = queryset.to_datetime(
                    datetime.fromtimestamp(int(timestamp_to))
                )
            except TypeError:
                return HttpResponseBadRequest('From needs to be in integer')

        queryset = self.get_query_by_page(queryset)
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
