# -*- coding: utf-8 -*-
from django.http import HttpResponse
from frontend.views import search_place
from localities.models import Country, Locality
from localities.utils import parse_bbox, get_heathsites_master
from .api_view import ApiView
from ..serializer.locality_serializer import json_serializer, geojson_serializer

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class LocalitySearchApiView(ApiView):
    """
    An API view class for retrieving facilities by search
    search it by place name of by facility name
    """

    def get_healthsite_master_by_polygon(self, polygon, facility_type):
        healthsites = get_heathsites_master().in_polygon(polygon)

        output = []
        index = 1
        for healthsite in healthsites:
            if healthsite.is_type(facility_type):
                if self.format == 'geojson':
                    output.append(geojson_serializer(healthsite))
                else:
                    output.append(json_serializer(healthsite))
                index += 1
            if index == self.limit:
                break
        return output

    def get(self, request, *args, **kwargs):
        super(LocalitySearchApiView, self).get(request)
        if 'name' not in request.GET or 'search_type' not in request.GET:
            return HttpResponse(
                self.formating_response({'error': "parameter is not enough"}),
                content_type='application/json')

        place_name = request.GET['name']
        search_type = request.GET['search_type']

        if not place_name:
            return HttpResponse(
                self.formating_response({'error': "place name parameter can't be empty"}),
                content_type='application/json')

        if search_type == "placename":
            try:
                country = Country.objects.get(name__icontains=place_name)
                polygon = country.polygon_geometry
            except Country.DoesNotExist:
                # if country is not found
                output = search_place(request, place_name)
                output['countries'] = ""
                bbox = output["southwest_lng"] + "," + \
                    output["southwest_lat"] + "," + \
                    output["northeast_lng"] + "," + \
                    output["northeast_lat"]
                try:
                    polygon = parse_bbox(bbox)
                except ValueError:
                    return HttpResponse(
                        self.formating_response({'error': "place is not found"}),
                        content_type='application/json')

            if 'facility_type' in request.GET:
                facility_type = request.GET['facility_type']
            else:
                facility_type = ""

            facilities = self.get_healthsite_master_by_polygon(polygon, facility_type)
            return HttpResponse(
                self.formating_response(facilities),
                content_type='application/json')

        elif search_type == "facility":
            facilities = Locality.objects.filter(name__icontains=place_name)
            facilities_dict = []
            for healthsite in facilities:
                if self.format == 'geojson':
                    facilities_dict.append(geojson_serializer(healthsite))
                else:
                    facilities_dict.append(json_serializer(healthsite))

            return HttpResponse(
                self.formating_response(facilities_dict),
                content_type='application/json')
        else:
            return HttpResponse(
                self.formating_response({'error': "search type is wrong"}),
                content_type='application/json')
