# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '15/04/19'

import json
import os
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView, Response


class GetMigrationProgress(APIView):
    """API to get the progress of data migration for a user."""

    def get(self, request):
        username = request.GET.get('username', None)
        if username:
            pathname = \
                os.path.join(
                    settings.CLUSTER_CACHE_DIR, 'data-migration-progress')
            progress_file = \
                os.path.join(pathname, '{}.txt'.format(username))
            found = os.path.exists(progress_file)

            if not found:
                return HttpResponseBadRequest('Data not found.')

            with open(progress_file) as json_file:
                data = json.load(json_file)
                return Response(data)
