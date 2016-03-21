# -*- coding: utf-8 -*-
import json
import logging
import uuid

LOG = logging.getLogger(__name__)
# register signals
from .forms import DataLoaderForm
from .map_clustering import cluster
from .models import Locality, Domain, Changeset, Value, Attribute, Specification
from .tasks import regenerate_cache
from .utils import parse_bbox, get_country_statistic, get_locality_detail, locality_create, locality_edit, \
    locality_updates, get_locality_by_spec_data

from braces.views import JSONResponseMixin, LoginRequiredMixin
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos import Point
from django.http import HttpResponse, Http404
from django.views.generic import DetailView, ListView, FormView
from localities.models import Country


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

        if not (all(param in request.GET for param in [
            'bbox', 'zoom', 'iconsize', 'geoname', 'tag', 'spec', 'data', 'uuid'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
            zoom = int(request.GET.get('zoom'))
            icon_size = map(int, request.GET.get('iconsize').split(','))
            geoname = request.GET.get('geoname')
            tag = request.GET.get('tag')
            spec = request.GET.get('spec')
            data = request.GET.get('data')
            uuid = request.GET.get('uuid')

        except:
            # return 404 if any of parameters are missing or not parsable
            raise Http404

        if zoom < 0 or zoom > 20:
            # zoom should be between 0 and 20
            raise Http404
        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise Http404

        return (bbox_poly, zoom, icon_size, geoname, tag, spec, data, uuid)

    def get(self, request, *args, **kwargs):
        # parse request params
        bbox, zoom, iconsize, geoname, tag, spec, data, uuid = self._parse_request_params(request)
        # cluster Localites for a view
        localities = Locality.objects.in_bbox(bbox)
        exception = False
        try:
            if geoname != "":
                # getting country's polygon
                country = Country.objects.get(
                        name__iexact=geoname)
                polygon = country.polygon_geometry
                localities = localities.in_polygon(polygon)
        except Country.DoesNotExist:
            if geoname != "" and geoname != "undefined":
                exception = True
            else:
                # searching by tag
                if tag != "" and tag != "undefined":
                    localities = Value.objects.filter(
                            specification__attribute__key='tags').filter(data__icontains="|" + tag + "|").values(
                            'locality')
                    localities = Locality.objects.filter(id__in=localities)
                else:
                    # serching by value
                    if spec != "" and spec != "undefined" and data != "" and data != "undefined":
                        localities = get_locality_by_spec_data(spec, data, uuid)
                        localities = Locality.objects.filter(id__in=localities)
        object_list = []
        focused = []
        if uuid:
            localities = localities.exclude(uuid=uuid)
            focused = Locality.objects.filter(uuid=uuid)
            focused = cluster(focused, zoom, *iconsize)
        if not exception:
            object_list = cluster(localities, zoom, *iconsize)
            if focused:
                object_list = object_list + focused
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
        if kwargs.has_key('changes'):
            obj_repr = get_locality_detail(self.object, kwargs['changes']);
        else:
            obj_repr = get_locality_detail(self.object, None);
        return self.render_json_response(obj_repr)


def get_json_from_request(request):
    # special request:
    special_request = ["long", "lat", "csrfmiddlewaretoken", "uuid"]

    mstring = []
    json = {}
    for key in request.POST.iterkeys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])

    for str in mstring:
        req = str.split('=', 1)
        json[req[0].lower()] = req[1]
        try:
            Attribute.objects.get(key=req[0].lower())
        except:
            if req[0] not in special_request:
                tmp_changeset = Changeset.objects.create(
                        social_user=request.user
                )
                attribute = Attribute()
                attribute.key = req[0]
                attribute.changeset = tmp_changeset
                attribute.save()
                domain = Domain.objects.get(name="Health")
                specification = Specification()
                specification.domain = domain
                specification.attribute = attribute
                specification.changeset = tmp_changeset
                specification.save()

    # check mandatory
    is_valid = True

    if not json['lat'] or json['lat'] == "":
        is_valid = False
        json['invalid_key'] = "latitude"

    if not json['long'] or json['long'] == "":
        is_valid = False
        json['invalid_key'] = "longitude"

    if is_valid:
        domain = Domain.objects.get(name="Health")
        attributes = Specification.objects.filter(domain=domain).filter(required=True)
        for attribute in attributes:
            try:
                if len(json[attribute.attribute.key]) == 0:
                    is_valid = False
                    json['invalid_key'] = attribute.attribute.key
                    break
            except:
                print "except"

    json['is_valid'] = is_valid
    return json


def locality_edit_view(request):
    return HttpResponse(json.dumps(locality_edit(request)))


def locality_create_view(request):
    return HttpResponse(json.dumps(locality_create(request)))


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
        if not request.user.is_superuser:
            raise Http404("Can not access this page")
        return super(DataLoaderView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Can not access this page")
        return super(DataLoaderView, self).post(request, *args, **kwargs)


def load_data(request):
    """Handling load data."""
    if request.method == 'POST':
        form = DataLoaderForm(request.POST, files=request.FILES,
                              user=request.user)
        if form.is_valid():
            data_loader = form.save(True)
            # load_data_task.delay(data_loader.pk)

            response = {}
            success_message = 'You have successfully upload your data'

            response['message'] = success_message
            response['success'] = True
            response['detailed_message'] = (
                'Please wait several minutes for Healthsites to load your data. We will send you an email if we '
                'have finished loading the data.'
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


def search_locality_by_name(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        locality_values = Value.objects.filter(
                specification__attribute__key='name').filter(
                data__istartswith=query)
        result = []
        for locality_value in locality_values:
            result.append(locality_value.data)
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json')


def search_locality_by_country(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        output = get_country_statistic(query)
        try:
            output['polygon'] = Country.objects.get(name__iexact=query).polygon_geometry.geojson
        except Country.DoesNotExist:
            print "empty"
        result = json.dumps(output, cls=DjangoJSONEncoder)

    return HttpResponse(result, content_type='application/json')


def search_countries(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        countries = Country.objects.filter(
                name__istartswith=query)
        result = []
        for country in countries:
            result.append(country.name)
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json')


def get_locality_update(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        uuid = request.GET.get('uuid')
        if date == "":
            date = datetime.now()
        locality = Locality.objects.get(uuid=uuid)
        last_updates = locality_updates(locality.id, date)
        output = []
        for last_update in last_updates:
            output.append({"last_update": last_update['changeset__created'],
                           "uploader": last_update['changeset__social_user__username'],
                           "nickname": last_update['nickname'],
                           "changeset_id": last_update['changeset']});
        result = json.dumps(output, cls=DjangoJSONEncoder)

    return HttpResponse(result, content_type='application/json')
