__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

import json
import os
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from api.api_views.v2.base_api import BaseAPIWithAuth
from rest_framework.response import Response
from api.utilities.clustering import oms_view_cluster
from api.utilities.geometry import parse_bbox
from localities.models import Country
from localities_osm.utilities import get_all_osm_query


class ErrorParameter(Exception):
    def __init__(self, message):
        super(ErrorParameter, self).__init__(message)
        self.errors = message


class GetCluster(BaseAPIWithAuth):
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
            icon_size = map(int, request.GET.get('iconsize').split(','))
            geoname = request.GET.get('geoname')
            max_zoom = int(request.GET.get('maxZoom'))
        except Exception as e:
            raise ErrorParameter('%s is needed in parameters' % e)

        if zoom < 0 or zoom > 20:
            raise ErrorParameter('zoom is incorrect')
        if any((size < 0 for size in icon_size)):
            raise ErrorParameter('iconsize needs to be positive')

        return (bbox_poly, zoom, max_zoom, icon_size, geoname)

    def get(self, request, *args, **kwargs):
        try:
            bbox, zoom, max_zoom, iconsize, geoname = self._parse_request_params(
                request
            )
        except ErrorParameter as e:
            return HttpResponseBadRequest('%s' % e)

        if not all([geoname]) and zoom <= settings.CLUSTER_CACHE_MAX_ZOOM:
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                '{}_{}_{}_localities.json'.format(zoom, *iconsize)
            )

            try:
                cached_locs = open(filename, 'rb')
                cached_data = json.loads(cached_locs.read())
                return Response(cached_data)
            except IOError:
                pass

        localities = get_all_osm_query().in_bbox(bbox)
        if geoname:
            try:
                # getting country's polygon
                country = Country.objects.get(
                    name__iexact=geoname)
                polygon = country.polygon_geometry
                localities = localities.in_polygon(polygon)
            except Country.DoesNotExist:
                pass
        return Response(
            oms_view_cluster(localities, zoom, max_zoom, *iconsize))
