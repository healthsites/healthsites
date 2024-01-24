__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

import json
import os
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.base_api import BaseAPI
from api.utilities.clustering import oms_view_cluster
from api.utilities.geometry import parse_bbox
from localities.models import Country
from localities_osm.queries import all_locality


class ErrorParameter(Exception):
    def __init__(self, message):
        super(ErrorParameter, self).__init__(message)
        self.errors = message


class GetCluster(BaseAPI):
    """
    Returns JSON representation of clustered points for the current map view

    Map view is defined by a *bbox*, *zoom* and *iconsize*
    """

    def _parse_request_params(self, request):
        """
        Try to parse arguments for a request and any error during parsing will
        raise Http404 exception
        """

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
            zoom = int(request.GET.get('zoom'))
            icon_size = [int(i) for i in request.GET.get('iconsize').split(',')]
            geoname = request.GET.get('geoname')
        except Exception as e:
            raise ErrorParameter('%s is needed in parameters' % e)

        if zoom < 0 or zoom > 20:
            raise ErrorParameter('zoom is incorrect')
        if any((size < 0 for size in icon_size)):
            raise ErrorParameter('iconsize needs to be positive')

        return (bbox_poly, zoom, icon_size, geoname)

    def get(self, request, *args, **kwargs):
        try:
            bbox, zoom, iconsize, geoname = self._parse_request_params(
                request
            )
        except ErrorParameter as e:
            return HttpResponseBadRequest('%s' % e)

        filters = json.loads(request.GET.get('filters', '{}'))

        if zoom <= settings.CLUSTER_CACHE_MAX_ZOOM and not filters:
            filename = f'{zoom}_{iconsize[0]}_{iconsize[1]}_localities.json'
            if geoname:
                filename = f'{zoom}_{iconsize[0]}_{iconsize[1]}_localities_{geoname}.json'
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                filename
            )

            try:
                cached_locs = open(filename, 'rb')
                cached_data = json.loads(cached_locs.read())
                return Response(cached_data)
            except IOError:
                pass

        localities = all_locality()
        if geoname:
            try:
                # getting country's polygon
                country = Country.objects.get(
                    name__iexact=geoname)
                localities = localities.in_administrative(country.get_codes)
            except Country.DoesNotExist:
                pass

        localities = localities.in_bbox(bbox)
        uuid = request.GET.get('uuid', None)
        if uuid:
            uuid = uuid.split('/')
            if len(uuid) == 2:
                try:
                    localities = localities.exclude(osm_type=uuid[0], osm_id=uuid[1])
                except ValueError:
                    pass
        localities = localities.in_filters(filters)
        return Response(
            oms_view_cluster(localities, zoom, *iconsize))
