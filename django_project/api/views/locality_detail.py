# -*- coding: utf-8 -*-
from django.http import HttpResponse
from localities.models import Locality
from .api_view import ApiView
from ..serializer.locality_serializer import json_serializer, \
    geojson_serializer


__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class LocalityDetailApiView(ApiView):
    """
    An API view class for retrieving facility detail
    """

    def get(self, request, *args, **kwargs):
        super(LocalityDetailApiView, self).get(request)
        if 'uuid' not in request.GET:
            return HttpResponse(
                self.formating_response({
                    'error': "parameter is not enough"
                }),
                content_type='application/json')
        uuid = request.GET['uuid']

        try:
            locality = Locality.objects.get(uuid=uuid)
        except Locality.DoesNotExist:
            return HttpResponse(
                self.formating_response({
                    'error': "facility isn't found"
                }),
                content_type='application/json'
            )

        if self.format == 'geojson':
            locality = [geojson_serializer(locality)]
        else:
            locality = json_serializer(locality)

        return HttpResponse(
            self.formating_response(locality),
            content_type='application/json')
