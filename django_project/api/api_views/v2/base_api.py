__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from api.authentication import APIKeyAuthentication\


class BaseAPI(APIView):
    _FORMATS = ['json', 'xml', 'geojson']
    format = 'json'

    def validation(self):
        self.format = self.request.GET.get('output', 'json')
        if self.format not in self._FORMATS:
            return '%s is not recognized' % self.format


class BaseAPIWithAuth(BaseAPI):
    authentication_classes = (SessionAuthentication, BasicAuthentication, APIKeyAuthentication)
