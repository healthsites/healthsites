__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/05/19'

import dicttoxml
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
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

