# coding=utf-8

__author__ = 'Muhammad Yarjuna Rohmat <myarjunar@kartoza.com>'
__date__ = '03/07/19'

import zlib

from api.api_views.v2.base_api import BaseAPIWithAuth
from rest_framework.views import Response


class GatherEnrollment(BaseAPIWithAuth):
    """API to get the Gather ODK server settings."""

    def get(self, request):
        user = request.user
        password = 'mock.password'
        server_url = 'mock.url'
        data = "{'username': '%s', 'password': '%s', 'server_url': '%s'}" % (
            user, password, server_url)
        compressed_data = zlib.compress(data, -1)
        return Response(compressed_data.encode('base64'))
