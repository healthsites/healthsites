__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import dicttoxml
from django.core.paginator import EmptyPage, Paginator
from rest_framework.views import APIView
from api.authentication import APIKeyAuthentication
from localities_healthsites_osm.serializer.locality import (
    LocalityHealthsitesOSMSerializer, LocalityHealthsitesOSMGeoSerializer)


class BaseAPI(APIView):
    authentication_classes = (APIKeyAuthentication,)
    _FORMATS = ['json', 'xml', 'geojson']
    format = 'json'

    # serializer
    JSONSerializer = LocalityHealthsitesOSMSerializer
    GEOJSONSerializer = LocalityHealthsitesOSMGeoSerializer

    def validation(self):
        self.format = self.request.GET.get('output', 'json')
        if self.format not in self._FORMATS:
            return '%s is not recognized' % self.format

    def serialize(self, queryset, many=False):
        if self.format == 'json':
            return self.JSONSerializer(queryset, many=many).data
        elif self.format == 'geojson':
            return self.GEOJSONSerializer(queryset, many=many).data
        elif self.format == 'xml':
            data = self.JSONSerializer(queryset, many=many).data
            return dicttoxml.dicttoxml(data)

    def parse_data(self, data):
        """ Parse raw data json to our structure of data
        :param data: raw data
        :type data: QueryDict

        :return: clean data
        :rtype: dict
        """
        data['lng'] = data['longitude']
        data['lat'] = data['latitude']
        del data['longitude']
        del data['latitude']

        # staff attributes
        nurse = ''
        doctors = ''
        try:
            nurse = data['nurses']
            del data['nurses']
        except KeyError:
            pass
        try:
            doctors = data['doctors']
            del data['doctors']
        except KeyError:
            pass
        data['staff'] = {
            'nurses': nurse,
            'doctors': doctors
        }

        # staff defining_hours
        sun = ''
        mon = ''
        tue = ''
        wed = ''
        thu = ''
        fri = ''
        sat = ''
        try:
            sun = data['sunday']
            del data['sunday']
        except KeyError:
            pass
        try:
            mon = data['monday']
            del data['monday']
        except KeyError:
            pass
        try:
            tue = data['tuesday']
            del data['tuesday']
        except KeyError:
            pass
        try:
            wed = data['wednesday']
            del data['wednesday']
        except KeyError:
            pass
        try:
            thu = data['thursday']
            del data['thursday']
        except KeyError:
            pass
        try:
            fri = data['friday']
            del data['friday']
        except KeyError:
            pass
        try:
            sat = data['saturday']
            del data['saturday']
        except KeyError:
            pass
        data['defining_hours'] = {
            'sun': sun,
            'mon': mon,
            'tue': tue,
            'wed': wed,
            'thu': thu,
            'fri': fri,
            'sat': sat
        }
        # staff inpatient_service
        full_time_beds = ''
        part_time_beds = ''
        try:
            full_time_beds = data['full_time_beds']
            del data['full_time_beds']
        except KeyError:
            pass
        try:
            part_time_beds = data['part_time_beds']
            del data['part_time_beds']
        except KeyError:
            pass
        data['inpatient_service'] = {
            'full_time_beds': full_time_beds,
            'part_time_beds': part_time_beds
        }

        # if using csrfmiddlewaretoken
        try:
            del data['csrfmiddlewaretoken']
        except KeyError:
            pass
        return data


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
