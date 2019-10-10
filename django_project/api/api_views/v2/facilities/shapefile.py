__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '17/12/19'

import json
import os
from django.http.response import HttpResponseBadRequest
from api.management.commands.generate_shapefile_countries import (
    get_shapefile_folder
)
from rest_framework.response import Response
from rest_framework.views import APIView
from localities.tasks import country_data_into_shapefile_task
from localities.models import Country
from localities_osm.models.locality import LocalityOSMView


class GetFacilitiesShapefileProcess(APIView):
    """
    API for checking process of generating shapefile
    """

    def get(self, request):
        try:
            country_name = request.GET['country']
        except KeyError:
            return HttpResponseBadRequest('country_name is needed on parameter')
        if country_name == 'world' or country_name == 'World':
            country_name = 'World'
        country_cache = get_shapefile_folder(country_name)
        metadata_file = os.path.join(country_cache, 'metadata')
        try:
            f = open(metadata_file, 'r')
            file_content = f.read()
            if file_content == 'Start':
                return Response('Start')
            try:
                metadata = json.loads(file_content)
            except ValueError:
                return Response('Start')
            if metadata['total'] >= metadata['index']:
                # check metadata
                if country_name == 'world' or country_name == 'World':
                    country_name = 'World'
                    queryset = LocalityOSMView.objects.all().order_by('row')
                else:
                    country = Country.objects.get(
                        name__iexact=country_name)
                    polygons = country.polygon_geometry
                    queryset = LocalityOSMView.objects.in_polygon(
                        polygons).order_by('row')
                if metadata['total'] == queryset.count() and \
                        metadata['last'] == queryset.last().osm_id:
                    return Response(metadata)
            else:
                return Response(metadata)
        except IOError:
            if not os.path.exists(country_cache):
                os.makedirs(country_cache)

        try:
            country_data_into_shapefile_task.delay(country_name)
            try:
                file = open(metadata_file, 'w+')
                file.write('Start')
                file.close()
            except Exception:
                pass
            return Response('Start')
        except Country.DoesNotExist:
            return HttpResponseBadRequest('%s is not found or not a country.' % country_name)
