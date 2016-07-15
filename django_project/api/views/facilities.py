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

    def get_heathsites_by_page(self, healthsites_query, page=1):
        try:
            healthsites = []
            paginator = Paginator(healthsites_query, 100)
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
        # checking page
        if 'page' not in request.GET:
            page = None
        else:
            try:
                page = request.GET.get('page')
                page = int(page)
                if page == 0:
                    return HttpResponse(
                        self.formating_response({'error': "page less than 1"}),
                        content_type='application/json')
            except ValueError:
                return HttpResponse(
                    self.formating_response({'error': "page is not a number"}),
                    content_type='application/json')

        # get data
        if 'extent' in request.GET:
            polygon = parse_bbox(request.GET.get('extent'))
            if not page:
                page = 1
            facilities = self.get_heathsites_by_page(get_heathsites_master().in_polygon(polygon), page)
            return HttpResponse(
                self.formating_response(facilities),
                content_type='application/json')
        elif 'page' in request.GET:
            if not page:
                return HttpResponse(
                    self.formating_response({'error': "page is wrong type"}),
                    content_type='application/json')
            facilities = self.get_heathsites_by_page(get_heathsites_master(), page)
            return HttpResponse(
                self.formating_response(facilities),
                content_type='application/json')
        else:
            return HttpResponse(
                self.formating_response({'error': "need parameter"}),
                content_type='application/json')