# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView, DetailView, ListView

from braces.views import JSONResponseMixin

from localities.models import Locality
from localities.utils import render_fragment


class MainView(TemplateView):
    template_name = 'main.html'


class LocalitiesLayer(JSONResponseMixin, ListView):
    def get_queryset(self):
        queryset = (
            Locality.objects.all()
        )
        return queryset

    def get(self, request, *args, **kwargs):
        object_list = [row.repr_simple() for row in self.get_queryset()]

        return self.render_json_response(object_list)


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
