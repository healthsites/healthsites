__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

import json
import os
from datetime import date
from hashlib import md5
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.db import connections, DatabaseError
from django.db.utils import ProgrammingError
from django.core.exceptions import FieldError
from api.api_views.v2.base_api import BaseAPI
from rest_framework.response import Response
from api.utilities.clustering import oms_view_cluster
from api.utilities.geometry import parse_bbox
from localities.models import Country
from localities_osm.queries import all_locality
from localities_osm.models.locality import LocalityOSMView


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
            icon_size = map(int, request.GET.get('iconsize').split(','))
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

        if zoom <= settings.CLUSTER_CACHE_MAX_ZOOM:
            filename = '{}_{}_{}_localities.json'.format(zoom, *iconsize)
            if geoname:
                filename = \
                    '{}_{}_{}_localities_{}.json'.format(
                        zoom, iconsize[0], iconsize[1], geoname)
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

        localities = all_locality().in_bbox(bbox)
        uuid = request.GET.get('uuid', None)
        if uuid:
            uuid = uuid.split('/')
            if len(uuid) == 2:
                try:
                    localities = localities.exclude(osm_type=uuid[0], osm_id=uuid[1])
                except ValueError:
                    pass
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
            oms_view_cluster(localities, zoom, *iconsize))


class FilterOSMData(BaseAPI):
    """Filters OSM data then returns the postgres view"""

    def get(self, request, *args, **kwargs):
        parameter_gets = request.GET.dict()
        filter_parameters = {}
        for get_key in parameter_gets:
            filter_parameters['{}__in'.format(get_key)] = (
                parameter_gets[get_key].split(',')
            )
        try:
            localities = LocalityOSMView.objects.filter(**filter_parameters)
        except FieldError as e:
            return Response(str(e))
        query_string = self.generate_query_string(localities)
        hashed_query_string = md5(query_string).hexdigest()
        view_name = 'osm-node-and-way-{}'.format(hashed_query_string)
        self.create_view(view_name, query_string)
        return Response(view_name)

    def generate_query_string(self, queryset):
        """
        Generate raw string of queryset.
        :param queryset: django queryset
        :return: raw query in string
        """
        raw_query = queryset.query.sql_with_params()
        if not raw_query:
            return
        formatted_params = ()
        params = raw_query[1]
        for param in params:
            formatted_param = param
            if (
                    isinstance(param, unicode)
                    or isinstance(param, int)  # noqa
                    or isinstance(param, date)   # noqa
            ):
                formatted_param = '\'' + str(param) + '\''
            elif isinstance(param, list):
                formatted_param = str(param)
                formatted_param = formatted_param.replace('[u\'', '\'{"')
                formatted_param = formatted_param.replace('\',', '",')
                formatted_param = formatted_param.replace(' u\'', ' "')
                formatted_param = formatted_param.replace('\']', '"}\'')
            formatted_params += (formatted_param,)
        query_string = raw_query[0] % formatted_params
        return query_string

    def create_view(self, name, sql_raw):
        """
        Create a postgres view, drop first if exist
        :param name: name of the view
        :param sql_raw: raw query in string
        """
        cursor = connections['docker_osm'].cursor()
        try:
            sql = (
                'DROP VIEW IF EXISTS "{view_name}"'.
                format(
                    view_name=name
                ))
            cursor.execute('''%s''' % sql)
        except (ProgrammingError, DatabaseError):
            pass
        sql = (
            'CREATE VIEW "{view_name}" AS {sql_raw}'.
            format(
                view_name=name,
                sql_raw=sql_raw
            ))
        cursor.execute('''%s''' % sql)
