__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import json
import dicttoxml
from django.core.paginator import EmptyPage, Paginator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from api.authentication import APIKeyAuthentication
from localities_osm.serializer.locality_osm import (
    LocalityOSMSerializer, LocalityOSMGeoSerializer)


class BaseAPI(APIView):
    _FORMATS = ['json', 'xml', 'geojson']
    format = 'json'

    # serializer
    JSONSerializer = LocalityOSMSerializer
    GEOJSONSerializer = LocalityOSMGeoSerializer

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
        used_data = data['attributes']
        used_data['name'] = data['name']
        used_data['lng'] = data['longitude']
        used_data['lat'] = data['latitude']
        del data['longitude']
        del data['latitude']

        # staff defining_hours
        sun = ''
        mon = ''
        tue = ''
        wed = ''
        thu = ''
        fri = ''
        sat = ''
        try:
            sun = data['attributes']['defining_hours']['sunday']
        except KeyError:
            pass
        try:
            mon = data['attributes']['defining_hours']['monday']
        except KeyError:
            pass
        try:
            tue = data['attributes']['defining_hours']['tuesday']
        except KeyError:
            pass
        try:
            wed = data['attributes']['defining_hours']['wednesday']
        except KeyError:
            pass
        try:
            thu = data['attributes']['defining_hours']['thursday']
        except KeyError:
            pass
        try:
            fri = data['attributes']['defining_hours']['friday']
        except KeyError:
            pass
        try:
            sat = data['attributes']['defining_hours']['saturday']
        except KeyError:
            pass
        used_data['defining_hours'] = {
            'sun': sun,
            'mon': mon,
            'tue': tue,
            'wed': wed,
            'thu': thu,
            'fri': fri,
            'sat': sat
        }

        # check schema
        schema = open('api/schema.json', 'rb')
        schema = json.loads(schema.read())
        for field in schema['facilities']['create']['fields']:
            if field['type'] == 'object':
                for key, prop in field['properties'].items():
                    try:
                        prop_value = used_data[prop['name']]
                    except KeyError:
                        continue
                    enum = None
                    if 'enum' in prop:
                        enum = prop['enum']
                    if prop['type'] == 'array':
                        if type(prop_value) != list:
                            raise ValueError('%s should be in list' % prop['name'])
                        if enum:
                            for value in prop_value:
                                if value not in enum:
                                    raise ValueError('%s is not recognized. Choices : %s' % (
                                        prop['name'], enum))
                    else:
                        if enum:
                            if prop_value not in enum:
                                raise ValueError('%s is not recognized. Choices : %s' % (
                                    prop['name'], enum))

        return used_data


class BaseAPIWithAuth(BaseAPI):
    authentication_classes = (SessionAuthentication, BasicAuthentication, APIKeyAuthentication)


class PaginationAPI(BaseAPIWithAuth):
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
