# -*- coding: utf-8 -*-
import logging
import json
import dicttoxml

LOG = logging.getLogger(__name__)

from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from braces.views import JSONResponseMixin

from localities.models import Locality
from localities.utils import parse_bbox

from .utils import remap_dict
from localities.views import getLocalityDetail
from django.core.serializers.json import DjangoJSONEncoder


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
        healthsites = Locality.objects.in_polygon(
                bbox_poly)
        output = []
        index = 1;

        facility_type = ""
        if 'facility_type' in request.GET:
            facility_type = request.GET['facility_type']

        for healthsite in healthsites:
            if healthsite.is_type(facility_type):
                output.append(healthsite.repr_dict())
                index += 1
            if index == 100:
                break
        return HttpResponse(formattedReturn(request, output), content_type='application/json')
