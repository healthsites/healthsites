# coding=utf-8
__author__ = 'Muhammad Yarjuna Rohmat <rohmat@kartoza.com>'
__date__ = '19/07/19'

import json
import os

from django.conf import settings
from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView, Response


class ImportCSVProgress(APIView):
    """API to get the progress of data import from csv."""
    exclude_from_docs = True

    def get(self, request):
        username = request.GET.get('username', request.user.username)
        if username:
            pathname = os.path.join(settings.CACHE_DIR, 'csv-import-progress')
            progress_file = os.path.join(pathname, '{}.txt'.format(username))

            if not os.path.exists(progress_file):
                return HttpResponseBadRequest('Data not found.')

            with open(progress_file) as json_file:
                data = json.load(json_file)
                return Response(data)
        else:
            return HttpResponseBadRequest('Username not provided.')
