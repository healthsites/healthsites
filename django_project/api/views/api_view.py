# -*- coding: utf-8 -*-

import json

import dicttoxml

from django.core.paginator import EmptyPage, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from api.serializer.locality_serializer import geojson_serializer, json_serializer


class ApiView(View):
    """ Abstract class that contains functions
    for healthsites API
    """
    _FORMATS = ['json', 'xml', 'geojson']
    format = 'json'
    limit = 100
    page = None

    def extract_request(self, request):
        """ Get function of api request
        override it to check format of api in request.

        :return: result of validation
        :rtype: str
        """
        if 'format' in request.GET:
            self.format = request.GET['format']
            if self.format not in self._FORMATS:
                self.format = 'json'

        # check page in request
        if 'page' in request.GET:
            try:
                page = request.GET.get('page')
                self.page = int(page)
                if self.page == 0:
                    return 'page less than 1'
            except ValueError:
                return 'page is not a number'

        return ''

    def get_query_by_page(self, query, page=1):
        """ Get query by page request
        :param query: query that will be paginated
        :type query: Queryset

        :param page: page index
        :type page: int

        :return: Paginated query
        """
        try:
            paginator = Paginator(query, self.limit)
            return paginator.page(page)
        except EmptyPage:
            return []

    def query_to_json(self, query, format):
        """ Format queryset to json
        :param query: query that will be formatted
        :type query: Queryset

        :param format: format type
        :type format: str

        :return: json based on format
        :rtype: dict
        """
        output = []
        for data in query:
            if format == 'geojson':
                output.append(geojson_serializer(data))
            else:
                output.append(json_serializer(data))
        return output

    def format_context(self, context):
        """ Function to format context that will be returned
        to http response
        :param context: context that will be formatted
        :type context: dict

        :return: formatted context
        :rtype: str
        """
        if self.format == 'xml':
            output = dicttoxml.dicttoxml(context)

        elif self.format == 'geojson':
            if not isinstance(context, list):
                context = [context]
            output = json.dumps(
                {'type': 'FeatureCollection', 'features': context},
                cls=DjangoJSONEncoder
            )

        else:
            output = json.dumps(context, cls=DjangoJSONEncoder)

        output.replace('|', ',')
        return output

    def api_response(self, context):
        """ Get return response from context
        :param context: context that will be returned
        :type context: dict

        :return: HTTP Response of context
        :rtype: HttpResponse
        """
        return HttpResponse(
            self.format_context(context),
            content_type='application/json')

    class Meta:
        abstract = True


class Docs(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            'https://github.com/healthsites/healthsites/wiki/API')
