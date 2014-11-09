# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import uuid

from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.db import transaction

from braces.views import JSONResponseMixin

from .models import Locality, Domain, Changeset
from .utils import render_fragment
from .forms import LocalityForm, DomainForm


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
            Locality.objects.select_related('domain')
        )
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        obj_repr = self.object.repr_dict()
        data_repr = render_fragment(
            self.object.domain.template_fragment, obj_repr
        )
        obj_repr.update({'repr': data_repr})

        return self.render_json_response(obj_repr)


class LocalityUpdate(SingleObjectMixin, FormView):
    form_class = LocalityForm
    template_name = 'updateform.html'

    def get_queryset(self):
        queryset = (
            Locality.objects.select_related('domain')
        )
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # update everything in one transaction
        with transaction.atomic():
            self.object.set_geom(
                form.cleaned_data.pop('lon'),
                form.cleaned_data.pop('lat')
            )
            self.object.save()
            self.object.set_values(
                form.cleaned_data, changeset=self.object.changeset
            )

            return HttpResponse('OK')

        # transaction failed
        return HttpResponse('ERROR updating Locality and values')

    def get_form(self, form_class):
        return form_class(locality=self.object, **self.get_form_kwargs())


class LocalityCreate(SingleObjectMixin, FormView):
    form_class = DomainForm
    template_name = 'updateform.html'

    def get_queryset(self):
        queryset = Domain.objects
        return queryset

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(name=self.kwargs.get('domain'))

        obj = queryset.get()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(LocalityCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # create new as a single transaction
        with transaction.atomic():
            tmp_changeset = Changeset.objects.create()

            tmp_uuid = uuid.uuid4().hex

            loc = Locality()
            loc.domain = self.object
            loc.uuid = tmp_uuid
            # generate unique upstream_id
            loc.upstream_id = u'web¶{}'.format(tmp_uuid)

            loc.geom = Point(
                form.cleaned_data.pop('lon'), form.cleaned_data.pop('lat')
            )
            loc.save()
            loc.set_values(form.cleaned_data, changeset=tmp_changeset)

            return HttpResponse(loc.pk)
        # transaction failed
        return HttpResponse('ERROR creating Locality and values')

    def get_form(self, form_class):
        return form_class(domain=self.object, **self.get_form_kwargs())
