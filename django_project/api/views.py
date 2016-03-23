# -*- coding: utf-8 -*-
import logging
import json
import dicttoxml

LOG = logging.getLogger(__name__)

from braces.views import JSONResponseMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from frontend.views import search_place
from localities.models import Country, Locality, Value
from localities.utils import parse_bbox, get_heathsite_by_polygon, limit, locality_create
from localities.views import get_locality_detail


def formattedReturn(request, value):
    try:
        format = request.GET['format']
    except Exception as e:
        try:
            format = request.POST['format']
        except Exception as e:
            format = 'json'

    if format == 'xml':
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
        value = get_locality_detail(locality, None)
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
                    data__icontains=place_name)
            print locality_values
            output = []
            index = 1;
            for locality in locality_values:
                guid = locality.locality.uuid
                locality = Locality.objects.get(uuid=guid)
                output.append(get_locality_detail(locality, None))
                index += 1
                if index == limit:
                    break
            return HttpResponse(formattedReturn(request, output), content_type='application/json')


class LocalityCreateAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['name'])):
            raise Http404

        return request

    def get(self, request, *args, **kwargs):
        return HttpResponse(formattedReturn(request, locality_create(request)), content_type='application/json')


class LoginAPI(JSONResponseMixin, View):
    slug_field = 'social'
    slug_url_kwarg = 'social'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponse("logged in", content_type='application/json')

        next = ""
        if 'next' in request.GET:
            next = '?next=%s' % request.GET['next']

        # check social
        social = kwargs['social']
        url = ""
        print social
        if social == "facebook":
            url = '/login/facebook/' + next
        elif social == "twitter":
            url = '/login/twitter/' + next
        elif social == "openstreetmap":
            url = '/login/openstreetmap/' + next
        elif social == "github":
            url = '/login/github/' + next
        elif social == "google":
            url = '/login/google-oauth2/' + next
        elif social == "linkedin":
            url = '/login/linkedin-oauth2/' + next

        # redirect to url
        if url != "":
            return HttpResponseRedirect(url)
        else:
            return HttpResponse("social name doesn't found", content_type='application/json')
