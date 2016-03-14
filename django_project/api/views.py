# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from braces.views import JSONResponseMixin

from localities.models import Locality
from localities.utils import parse_bbox

from .utils import remap_dict
from localities.views import getLocalityDetail
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


class LocalitiesAPI(JSONResponseMixin, View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['bbox'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
        except:
            # return 404 if any of parameters are missing or not parsable
            raise Http404

        return bbox_poly

    def get(self, request, *args, **kwargs):
        bbox = self._parse_request_params(request)
        # iterate thorugh queryset and remap keys
        transform = {
            'changeset__social_user_id': 'user_id'
        }
        object_list = [
            remap_dict(loc, transform)
            for loc in Locality.objects.in_bbox(bbox)
                .select_related('changeset')
                .get_lnglat()
                .values(
                    'uuid', 'lnglat', 'version', 'changeset__social_user_id',
                    # 'changeset__created'
            )
            ]

        return self.render_json_response(object_list)


class LocalityAPI(JSONResponseMixin, SingleObjectMixin, View):
    model = Locality
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_json_response(self.object.repr_dict())


def LocalityDetail(request):
    if request.method == 'GET':
        try:
            locality = Locality.objects.get(uuid=request.GET['guid'])
            output = getLocalityDetail(locality, None)
            output = json.dumps(output, cls=DjangoJSONEncoder)

            try:
                format = request.GET['format']
            except Exception as e:
                format = 'json'

            if format == 'json':
                return HttpResponse(output, content_type='application/json')

            elif format == 'xml':
                print output
                output = serializers.serialize('xml', output, fields=('name', 'size'))
                return HttpResponse(output, content_type='application/json')

            return HttpResponse(output)
        except Locality.DoesNotExist:
            raise Http404
        except Exception as e:
            print e
            return HttpResponse(status=500)
