__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/05/19'

import dicttoxml
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.core.paginator import EmptyPage, Paginator
from api.api_views.v2.base_api import BaseAPI
from api.authentication import APIKeyAuthentication
from localities_osm.serializer.locality_osm import (
    LocalityOSMSerializer, LocalityOSMGeoSerializer)


class FacilitiesBaseAPI(BaseAPI):
    # serializer
    JSONSerializer = LocalityOSMSerializer
    GEOJSONSerializer = LocalityOSMGeoSerializer

    def serialize(self, queryset, many=False):
        if self.format == 'json':
            return self.JSONSerializer(queryset, many=many).data
        elif self.format == 'geojson':
            return self.GEOJSONSerializer(queryset, many=many).data
        elif self.format == 'xml':
            data = self.JSONSerializer(queryset, many=many).data
            return dicttoxml.dicttoxml(data)


class FacilitiesBaseAPIWithAuth(FacilitiesBaseAPI):
    authentication_classes = (SessionAuthentication, BasicAuthentication, APIKeyAuthentication)


class PaginationAPI(FacilitiesBaseAPIWithAuth):
    """
    Base API for Facilities in pagination
    """
    limit = 100
    page = None

    def validation(self):
        """ Validate request of the API

        :return: return error on request
        :rtype: str
        """
        validation = super(PaginationAPI, self).validation()
        if validation:
            return validation

        data = self.request.GET
        page = data.get('page', 1)
        try:
            self.page = int(page)
            if self.page <= 0:
                return 'page less than 1'
        except ValueError:
            return 'page is not a number'
        return None

    def get_query_by_page(self, query):
        """ Get query by page request
        :param query: query that will be paginated
        :type query: Queryset

        :param page: page index
        :type page: int

        :return: Paginated query
        """
        try:
            paginator = Paginator(query, self.limit)
            return paginator.page(self.page)
        except EmptyPage:
            return []
