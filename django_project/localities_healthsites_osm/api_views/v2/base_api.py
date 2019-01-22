__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import dicttoxml
from django.core.paginator import EmptyPage, Paginator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from localities_healthsites_osm.serializer.locality import (
    LocalityHealthsitesOSMSerializer,
    LocalityHealthsitesOSMGeoSerializer)
from localities_healthsites_osm.api_views.v2 import (
    CsrfExemptSessionAuthentication
)


class BaseAPI(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    _FORMATS = ['json', 'xml', 'geojson']
    format = 'json'

    def validation(self):
        self.format = self.request.GET.get('output', 'json')
        if self.format not in self._FORMATS:
            return '%s is not recognized' % self.format

    def serialize(self, queryset, many=False):
        if self.format == 'json':
            return LocalityHealthsitesOSMSerializer(
                queryset, many=many).data
        elif self.format == 'geojson':
            return LocalityHealthsitesOSMGeoSerializer(
                queryset, many=many).data
        elif self.format == 'xml':
            data = LocalityHealthsitesOSMSerializer(
                queryset, many=many).data
            return dicttoxml.dicttoxml(data)


class PaginationAPI(BaseAPI):
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
