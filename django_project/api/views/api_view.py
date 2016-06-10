__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.views.generic import View
import json
import dicttoxml

from django.core.serializers.json import DjangoJSONEncoder


class ApiView(View):
    limit = 100
    formats = ['json', 'xml', 'geojson']
    format = 'json'

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            if 'format' in request.GET:
                self.format = request.GET['format']
                if not self.format in self.formats:
                    self.format = 'json'

    def formating_response(self, response):
        if self.format == 'xml':
            output = dicttoxml.dicttoxml(response)
        elif self.format == 'geojson':
            output = json.dumps({"type": "FeatureCollection", "features": response}, cls=DjangoJSONEncoder)
        else:
            output = json.dumps(response, cls=DjangoJSONEncoder)
        print output
        output.replace("|", ",")
        print output
        return output
