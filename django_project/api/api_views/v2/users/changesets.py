__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/05/19'

from django.http.response import HttpResponseBadRequest
from rest_framework.views import Response
from api.api_views.v2.pagination import (
    PaginationAPI, LessThanOneException, NotANumberException
)
from localities_osm.models.locality import LocalityOSMView
from localities_osm.serializer.locality_osm import LocalityOSMBasicSerializer
from localities_osm.utilities import get_all_osm_query


class GetChangesets(PaginationAPI):
    def get(self, request, username):
        updates_osm = get_all_osm_query().filter(
            changeset_user=username).exclude(
            changeset_timestamp__isnull=True).order_by(
            '-changeset_timestamp')

        try:
            queryset = self.get_query_by_page(updates_osm)
        except (LessThanOneException, NotANumberException) as e:
            return HttpResponseBadRequest('%s' % e)

        return Response(
            LocalityOSMBasicSerializer(queryset, many=True).data)
