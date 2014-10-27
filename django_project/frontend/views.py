# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView, DetailView

from braces.views import JSONResponseMixin

from djgeojson.views import GeoJSONLayerView


from localities.models import Locality
from localities.utils import render_fragment


class MainView(TemplateView):
    template_name = 'main.html'


class LocalitiesLayer(GeoJSONLayerView):
    # precision = 4   # float
    model = Locality
    # properties = ['id']


class LocalityInfo(JSONResponseMixin, DetailView):
    model = Locality

    def get_queryset(self):
        queryset = (
            Locality.objects.select_related('group')
        )
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        obj_repr = self.object.repr_dict()
        data_repr = render_fragment(
            self.object.group.template_fragment, obj_repr
        )
        obj_repr.update({'repr': data_repr})

        return self.render_json_response(obj_repr)
