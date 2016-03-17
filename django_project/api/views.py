# -*- coding: utf-8 -*-
import logging
import json
import dicttoxml

LOG = logging.getLogger(__name__)

from django.http import Http404, HttpResponse
from django.views.generic import View
from braces.views import JSONResponseMixin
from localities.utils import parse_bbox
from localities.views import getLocalityDetail
from frontend.views import search_place
from django.core.serializers.json import DjangoJSONEncoder
from localities.models import Locality, Value, Country


def formattedReturn(request, value):
    try:
        format = request.GET['format']
    except Exception as e:
        format = 'json'

    if format == 'xml':
        print value
        output = dicttoxml.dicttoxml(value)
    else:
        output = json.dumps(value, cls=DjangoJSONEncoder)
    return output


class LocalityAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['guid'])):
            raise Http404
        return request.GET['guid']

    def get(self, request, *args, **kwargs):
        guid = self._parse_request_params(request)
        locality = Locality.objects.get(uuid=guid)
        value = getLocalityDetail(locality, None)
        return HttpResponse(formattedReturn(request, value), content_type='application/json')


def get_heathsite_by_polygon(request, polygon):
    healthsites = Locality.objects.in_polygon(
            polygon)

    facility_type = ""
    if 'facility_type' in request.GET:
        facility_type = request.GET['facility_type']

    output = []
    index = 1;
    for healthsite in healthsites:
        if healthsite.is_type(facility_type):
            output.append(healthsite.repr_dict())
            index += 1
        if index == 100:
            break
    return output


class LocalitiesAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['extent'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('extent'))
        except Exception as e:
            raise Http404
        return bbox_poly

    def get(self, request, *args, **kwargs):
        bbox_poly = self._parse_request_params(request)
        return HttpResponse(formattedReturn(request, get_heathsite_by_polygon(request, bbox_poly)),
                            content_type='application/json')


class LocalitySearchAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['search_type', 'name'])):
            raise Http404

        if not request.GET['search_type'] in ["facility", "placename"]:
            raise Http404

        return request

    def get(self, request, *args, **kwargs):
        place_name = request.GET['name']
        search_type = request.GET['search_type']

        if search_type == "placename":
            try:
                country = Country.objects.get(name__icontains=place_name)
                polygon = country.polygon_geometry
            except Exception as e:
                # if country is not found
                output = search_place(request, place_name)
                output['countries'] = ""
                bbox = output["southwest_lng"] + "," + output["southwest_lat"] + "," + output["northeast_lng"] + "," + \
                       output["northeast_lat"]
                try:
                    polygon = parse_bbox(bbox)
                except Exception as e:
                    raise Http404
            return HttpResponse(formattedReturn(request, get_heathsite_by_polygon(request, polygon)),
                                content_type='application/json')

        if search_type == "facility":
            locality_values = Value.objects.filter(
                    specification__attribute__key='name').filter(
                    data=place_name)
            if locality_values:
                locality_value = locality_values[0]
            else:
                locality_values = Value.objects.filter(
                        specification__attribute__key='name').filter(
                        data__istartswith=place_name)
                if locality_values:
                    locality_value = locality_values[0]
                else:
                    raise Http404
            guid = locality_value.locality.uuid
            locality = Locality.objects.get(uuid=guid)
            value = getLocalityDetail(locality, None)
            return HttpResponse(formattedReturn(request, value), content_type='application/json')
