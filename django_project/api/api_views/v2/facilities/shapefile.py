__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '17/12/19'

import os
from django.conf import settings
from django.http.response import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from localities.tasks import country_data_into_shapefile_task


class GetShapefileDetail(APIView):
    """
    API for checking process of generating shapefile
    """

    def get(self, request, country):
        if country == 'World' or country == 'world':
            country = 'World'

        # check if shapefile is exist or not
        filename = '%s.zip' % country
        file_path = os.path.join(settings.SHAPEFILE_DIR, filename)
        if os.path.exists(file_path):
            return Response({
                'time': os.path.getmtime(file_path),
                'filename': filename
            })
        else:
            raise Http404()


class GetShapefileDownload(APIView):
    """
    API for checking process of generating shapefile
    """

    def get(self, request, country):
        if country == 'World' or country == 'world':
            country = 'World'
        country_data_into_shapefile_task.delay(country)
        filename = '%s.zip' % country
        file_path = os.path.join(settings.SHAPEFILE_DIR, filename)

        if os.path.exists(file_path):
            test_file = open(file_path, 'rb')
            response = HttpResponse(content=test_file)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
            return response
        else:
            raise Http404()
