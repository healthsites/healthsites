__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/05/19'

from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest
from rest_framework.views import Response
from api.api_views.v2.pagination import (
    PaginationAPI, LessThanOneException, NotANumberException
)
from localities_osm.serializer.locality_osm import LocalityOSMBasicSerializer
from localities_osm.queries import all_locality
from social_users.utils import get_osm_name


class GetChangesets(PaginationAPI):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            osm_user = get_osm_name(user)
            if osm_user:
                username = osm_user
        except User.DoesNotExist:
            pass

        updates_osm = all_locality().filter(
            changeset_user=username).exclude(
            changeset_timestamp__isnull=True).order_by(
            '-changeset_timestamp')

        try:
            queryset = self.get_query_by_page(updates_osm)
        except (LessThanOneException, NotANumberException) as e:
            return HttpResponseBadRequest('%s' % e)

        return Response(
            LocalityOSMBasicSerializer(queryset, many=True).data)
