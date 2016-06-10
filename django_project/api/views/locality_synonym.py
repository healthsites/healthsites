# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'
from django.http import HttpResponse
from frontend.views import search_place
from localities.models import Country, Locality, SynonymLocalities
from localities.utils import parse_bbox
from .api_view import ApiView
from ..serializer.locality_serializer import json_serializer, geojson_serializer


class LocalitySynonymApiView(ApiView):
    """
    An API vuew class for retrieving facilities by search
    search it by place name of by facility name
    """

    def get(self, request, *args, **kwargs):
        super(LocalitySynonymApiView, self).get(request)
        if not 'uuid' in request.GET:
            return HttpResponse(
                self.formating_response({'error': "parameter is not enough"}),
                content_type='application/json')
        uuid = request.GET['uuid']

        try:
            locality = Locality.objects.get(uuid=uuid)
        except Locality.DoesNotExist:
            return HttpResponse(self.formating_response({'error': "facility isn't found"}),
                                content_type='application/json')

        synonyms = SynonymLocalities.objects.filter(locality=locality)
        facilities_dict = []
        for synonym in synonyms:
            if self.format == 'geojson':
                facilities_dict.append(geojson_serializer(synonym.synonym))
            else:
                facilities_dict.append(json_serializer(synonym.synonym))
        return HttpResponse(
            self.formating_response(facilities_dict),
            content_type='application/json')
