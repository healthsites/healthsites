# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.http import HttpResponse
from localities.models import Locality
from .api_view import ApiView
from ..serializer.locality_serializer import json_serializer, geojson_serializer


class LocalityDetailApiView(ApiView):
    """ An API view class for retrieving facility detail
    """

    def get(self, request, *args, **kwargs):
        validation = self.extract_request(request)
        if validation:
            return self.api_response(
                {'error': validation}
            )

        # check uuid for this
        if 'uuid' not in request.GET:
            return self.api_response(
                {'error': "parameter is not enough"}
            )

        uuid = request.GET['uuid']
        try:
            facilities = Locality.objects.get(uuid=uuid)
        except Locality.DoesNotExist:
            return self.api_response(
                {'error': "facility isn't found"}
            )

        facilities = self.query_to_json([facilities], self.format)

        return self.api_response(facilities[0])
