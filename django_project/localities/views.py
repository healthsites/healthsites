# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import uuid
import json
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, Http404
from django.contrib.gis.geos import Point
from django.db import transaction

from braces.views import JSONResponseMixin, LoginRequiredMixin

from .models import Locality, Domain, Changeset
from .utils import render_fragment, parse_bbox
from .forms import LocalityForm, DomainForm, DataLoaderForm
from .importers import CSVImporter

from .map_clustering import cluster


class LocalitiesLayer(JSONResponseMixin, ListView):
    """
    Returns JSON representation of clustered points for the current map view

    Map view is defined by a *bbox*, *zoom* and *iconsize*
    """

    def _parse_request_params(self, request):
        """
        Try to parse arguments for a request and any error during parsing will
        raise Http404 exception
        """

        if not(all(param in request.GET for param in [
                'bbox', 'zoom', 'iconsize'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
            zoom = int(request.GET.get('zoom'))
            icon_size = map(int, request.GET.get('iconsize').split(','))

        except:
            # return 404 if any of parameters are missing or not parsable
            raise Http404

        if zoom < 0 or zoom > 20:
            # zoom should be between 0 and 20
            raise Http404
        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise Http404

        return (bbox_poly, zoom, icon_size)

    def get(self, request, *args, **kwargs):
        # parse request params
        bbox, zoom, iconsize = self._parse_request_params(request)

        # cluster Localites for a view
        object_list = cluster(Locality.objects.in_bbox(bbox), zoom, *iconsize)

        return self.render_json_response(object_list)


class LocalityInfo(JSONResponseMixin, DetailView):
    """
    Returns JSON representation of an Locality object (repr_dict) and a
    rendered template fragment (repr)
    """

    model = Locality
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

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


class LocalityUpdate(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    Handles Locality updates, users need to be logged in order to update a
    Locality
    """

    raise_exception = True
    form_class = LocalityForm
    template_name = 'updateform.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

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
            if self.object.tracker.changed():
                # there are some changes so create a new changeset
                tmp_changeset = Changeset.objects.create(
                    social_user=self.request.user
                )
                self.object.changeset = tmp_changeset
            self.object.save()
            self.object.set_values(
                form.cleaned_data, social_user=self.request.user
            )

            return HttpResponse('OK')

        # transaction failed
        return HttpResponse('ERROR updating Locality and values')

    def get_form(self, form_class):
        return form_class(locality=self.object, **self.get_form_kwargs())


class LocalityCreate(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    Handles Locality creates, users need to be logged in order to create a
    Locality
    """

    raise_exception = True
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
            tmp_changeset = Changeset.objects.create(
                social_user=self.request.user
            )

            # generate new uuid
            tmp_uuid = uuid.uuid4().hex

            loc = Locality()
            loc.changeset = tmp_changeset
            loc.domain = self.object
            loc.uuid = tmp_uuid

            # generate unique upstream_id
            loc.upstream_id = u'web¶{}'.format(tmp_uuid)

            loc.geom = Point(
                form.cleaned_data.pop('lon'), form.cleaned_data.pop('lat')
            )
            loc.save()
            loc.set_values(form.cleaned_data, social_user=self.request.user)

            return HttpResponse(loc.pk)
        # transaction failed
        return HttpResponse('ERROR creating Locality and values')

    def get_form(self, form_class):
        return form_class(domain=self.object, **self.get_form_kwargs())


class DataLoaderView(LoginRequiredMixin, FormView):
    """Handles DataLoader.
    """
    form_class = DataLoaderForm
    template_name = 'dataloaderform.html'

    def get_form(self, form_class):
        return form_class()

    def form_valid(self, form):
        pass

    def get(self, request, *args, **kwargs):
        return super(DataLoaderView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(DataLoaderView, self).post(request, *args, **kwargs)


def load_data(request):
    """Handling load data."""
    if request.method == 'POST':
        form = DataLoaderForm(request.POST, files=request.FILES,
                              user=request.user)
        if form.is_valid():
            data_loader = form.save(True)

            # Data Processing
            csv_importer = CSVImporter(
                'Health',
                data_loader.organisation_name,
                data_loader.csv_data.path,
                data_loader.json_concept_mapping.path,
                use_tabs=False,
                user=data_loader.author,
                mode=data_loader.data_loader_mode
            )

            data_loader.applied = True
            data_loader.save()

            response = {}
            success_message = 'You have successfully load data'
            response['created'] = csv_importer.report['created']
            response['modified'] = csv_importer.report['modified']
            response['duplicated'] = csv_importer.report['duplicated']

            response['message'] = success_message
            response['success'] = True
            response['detailed_message'] = (
                'There are %s localities created and %s localities modified.'
                % (response['created'], response['modified'])
            )
            if response['duplicated'] > 0:
                response['detailed_message'] += (
                    ' You also have %s possible duplicated localities, '
                    'and they are not added.' % response['duplicated']
                )
            return HttpResponse(json.dumps(
                response,
                ensure_ascii=False),
                content_type='application/javascript')
        else:
            error_message = form.errors
            response = {
                'detailed_message': str(error_message),
                'success': False,
                'message': 'You have failed to load data.'
            }
            return HttpResponse(json.dumps(
                response,
                ensure_ascii=False),
                content_type='application/javascript')
    else:
        pass
