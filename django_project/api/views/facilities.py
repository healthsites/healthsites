# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponse
from localities.utils import parse_bbox, get_heathsites_master
from ..serializer.locality_serializer import json_serializer, geojson_serializer
from .api_view import ApiView


class FacilitiesApiView(ApiView):
    """
    An API vuew class for retrieving facilities
    It retruns facilties regarding parameter :
    - extent : a geometry
    - page : returns 100 facilities for each of page
    """

    def get_heathsites_master_by_page(self, page):
        try:
            healthsites = []
            paginator = Paginator(get_heathsites_master(), 100)
            page = paginator.page(page)
            for healthsite in page:
                if self.format == 'geojson':
                    healthsites.append(geojson_serializer(healthsite))
                else:
                    healthsites.append(json_serializer(healthsite))
        except EmptyPage:
            healthsites = []
        return healthsites

    def get(self, request, *args, **kwargs):
        super(FacilitiesApiView, self).get(request)
        if 'extent' in request.GET:
            polygon = parse_bbox(request.GET.get('extent'))
            facilities = get_heathsites_master().in_polygon(polygon)
        elif 'page' in request.GET:
            page = request.GET.get('page')
            try:
                page = int(page)
                if page == 0:
                    return HttpResponse(
                        self.formating_response({'error': "page less than 1"}),
                        content_type='application/json')
                facilities = self.get_heathsites_master_by_page(page)
                return HttpResponse(
                    self.formating_response(facilities),
                    content_type='application/json')

            except ValueError:
                return HttpResponse(
                    self.formating_response({'error': "page is not a number"}),
                    content_type='application/json')
        else:
            return HttpResponse(
                self.formating_response({'error': "need parameter"}),
                content_type='application/json')

        facilities_dict = []
        for healthsite in facilities:
            if self.format == 'geojson':
                facilities_dict.append(geojson_serializer(healthsite))
            else:
                facilities_dict.append(json_serializer(healthsite))

        return HttpResponse(
            self.formating_response(facilities_dict),
            content_type='application/json')
