# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse

from braces.views import JSONResponseMixin

from .models import Locality
from .utils import render_fragment
from .forms import LocalityForm


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


class LocalityUpdate(JSONResponseMixin, SingleObjectMixin, FormView):
    form_class = LocalityForm
    template_name = 'updateform.html'

    def get_queryset(self):
        queryset = (
            Locality.objects.select_related('group')
        )
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.set_geom(
            form.cleaned_data.pop('lon'), form.cleaned_data.pop('lat')
        )
        self.object.save()
        self.object.set_values(form.cleaned_data)

        return HttpResponse('OK')

    def get_form(self, form_class):
        return form_class(locality=self.object, **self.get_form_kwargs())
