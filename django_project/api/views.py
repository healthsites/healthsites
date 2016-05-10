# -*- coding: utf-8 -*-
import logging
import json
import dicttoxml

LOG = logging.getLogger(__name__)

from braces.views import JSONResponseMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse
from django.views.generic import View
from frontend.views import search_place
from localities.models import Country, Locality, UnconfirmedSynonym, Value
from localities.utils import parse_bbox, get_heathsites_master_by_polygon, get_heathsites_master_by_page, \
    get_heathsites_synonyms, limit, \
    locality_create
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
        if 'guid' in request.GET:
            return request.GET['guid']
        elif 'uuid' in request.GET:
            return request.GET['uuid']
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        uuid = self._parse_request_params(request)
        try:
            locality = Locality.objects.get(uuid=uuid)
        except Locality.DoesNotExist:
            return HttpResponse(formattedReturn(request, {'error': "facility doesn't exist"}),
                                content_type='application/json')
        value = get_locality_detail(locality, None)
        return HttpResponse(formattedReturn(request, value), content_type='application/json')


class LocalitySynonymsAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if 'guid' in request.GET:
            return request.GET['guid']
        elif 'uuid' in request.GET:
            return request.GET['uuid']
        else:
            # raise Http404
            return None

    def get(self, request, *args, **kwargs):
        uuid = self._parse_request_params(request)
        if uuid:
            try:
                locality = Locality.objects.get(uuid=uuid)
            except Locality.DoesNotExist:
                return HttpResponse(formattedReturn(request, {'error': "facility doesn't exist"}),
                                    content_type='application/json')
        else:
            return HttpResponse(formattedReturn(request, get_heathsites_synonyms()),
                                content_type='application/json')

        value = []
        for synonym in locality.get_synonyms():
            value.append(get_locality_detail(synonym, None))
        return HttpResponse(formattedReturn(request, value), content_type='application/json')


class LocalitiesAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['extent', 'page'])):
            raise Http404

        return request

    def get(self, request, *args, **kwargs):
        if 'extent' in request.GET:
            try:
                bbox_poly = parse_bbox(request.GET.get('extent'))
                return HttpResponse(formattedReturn(request, get_heathsites_master_by_polygon(request, bbox_poly)),
                                    content_type='application/json')
            except Exception as e:
                raise Http404
        elif 'page' in request.GET:
            page = request.GET.get('page')
            try:
                page = int(page)
                if page == 0:
                    return HttpResponse(formattedReturn(request, {'error': "page less than 1"}),
                                        content_type='application/json')
                return HttpResponse(formattedReturn(request, get_heathsites_master_by_page(page)),
                                    content_type='application/json')
            except ValueError:
                return HttpResponse(formattedReturn(request, {'error': "page is not a number"}),
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
            return HttpResponse(formattedReturn(request, get_heathsites_master_by_polygon(request, polygon)),
                                content_type='application/json')

        if search_type == "facility":
            locality_values = Value.objects.filter(
                specification__attribute__key='name').filter(
                data__icontains=place_name)
            output = []
            index = 1;
            for locality in locality_values:
                uuid = locality.locality.uuid
                locality = Locality.objects.get(uuid=uuid)
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


from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class LocalityCreateAPIStrict(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['geom'])):
            raise Http404

        return request.GET['geom']

    def get(self, request, *args, **kwargs):
        geom = self._parse_request_params(request)
        request.session['new_geom'] = geom
        map_url = reverse('map')
        return HttpResponseRedirect(map_url)


class LocalityReportDuplicate(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        if 'master' not in request.POST:
            return HttpResponse(formattedReturn(request, {'error': "master uuid parameter isn't provided"}),
                                content_type='application/json')
        if 'synonym' not in request.POST:
            return HttpResponse(formattedReturn(request, {'error': "synonym uuid parameter isn't provided"}),
                                content_type='application/json')

        master = request.POST['master']
        try:
            master = Locality.objects.get(uuid=master)
        except Locality.DoesNotExist:
            return HttpResponse(formattedReturn(request, {'error': "master is not found"}),
                                content_type='application/json')

        synonym = request.POST['synonym']
        try:
            synonym = Locality.objects.get(uuid=synonym)
        except Locality.DoesNotExist:
            return HttpResponse(formattedReturn(request, {'error': "synonym is not found"}),
                                content_type='application/json')

        if synonym == master:
            return HttpResponse(formattedReturn(request, {'error': "cannot assign duplication to itself"}),
                                content_type='application/json')

        try:
            UnconfirmedSynonym.objects.get(locality=master, synonym=synonym)
        except UnconfirmedSynonym.DoesNotExist:
            UnconfirmedSynonym(locality=master, synonym=synonym).save()

        return HttpResponse(formattedReturn(request, {'success': "report has submitted"}),
                            content_type='application/json')
