# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import uuid
import json
# register signals
import signals  # noqa
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.gis.geos import Point
from django.db import transaction
from django.conf import settings
from braces.views import JSONResponseMixin, LoginRequiredMixin
import googlemaps
from .models import Locality, Domain, Changeset, Value, Attribute, Specification
from .utils import render_fragment, parse_bbox
from .forms import LocalityForm, DomainForm, DataLoaderForm, SearchForm
from .tasks import load_data_task, test_task
from .map_clustering import cluster
import logging
from localities.models import Country
from django.db.models import Count

LOG = logging.getLogger(__name__)


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
            'bbox', 'zoom', 'iconsize', 'geoname'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
            zoom = int(request.GET.get('zoom'))
            icon_size = map(int, request.GET.get('iconsize').split(','))
            geoname = request.GET.get('geoname');

        except:
            # return 404 if any of parameters are missing or not parsable
            raise Http404

        if zoom < 0 or zoom > 20:
            # zoom should be between 0 and 20
            raise Http404
        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise Http404

        return (bbox_poly, zoom, icon_size, geoname)

    def get(self, request, *args, **kwargs):
        # parse request params
        bbox, zoom, iconsize, geoname = self._parse_request_params(request)
        # cluster Localites for a view
        locatities = Locality.objects.in_bbox(bbox)
        exception = False
        try:
            if geoname != "":
                # getting country's polygon
                country = Country.objects.get(
                    name__iexact=geoname)
                polygon = country.polygon_geometry
                locatities = locatities.in_polygon(polygon)
        except Country.DoesNotExist:
            if geoname != "" and geoname != "undefined":
                exception = True

        object_list = []
        if not exception:
            object_list = cluster(locatities, zoom, *iconsize)

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
        # get attributes
        attribute_count = Attribute.objects.all().count() + 1  # geom
        # count completeness based attributes
        obj_repr = self.object.repr_dict()
        data_repr = render_fragment(
            self.object.domain.template_fragment, obj_repr
        )
        obj_repr.update({'repr': data_repr})
        num_data = len(obj_repr['values']) + 1  # geom
        completeness = (num_data + 0.0) / (attribute_count + 0.0) * 100  # percentage
        obj_repr.update({'completeness': '%s%%' % format(completeness, '.2f')})

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


def locality_edit(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            request_uuid = request.POST.get('uuid')
            request_lat = request.POST.get('lat')
            request_long = request.POST.get('long')
            request_name = request.POST.get('locality-name')
            request_physical_address = request.POST.get('physical-address')
            request_phone = request.POST.get('phone')
            request_operation = request.POST.get('operation')
            request_nature = request.POST.get('nature-of-facility')
            request_scope = request.POST.get('scope-of-service')
            request_ancillary = request.POST.get('ancillary')
            request_ownership = request.POST.get('ownership')
            request_activities = request.POST.get('activities')
            request_inpatient = request.POST.get('inpatient-service')
            request_staff = request.POST.get('staff')

            locality = Locality.objects.get(uuid=request_uuid)
            json = {}
            json['name'] = request_name
            json['physical_address'] = request_physical_address
            json['phone'] = request_phone
            json['operation'] = request_operation
            json['nature_of_facility'] = request_nature
            json['scope_of_service'] = request_scope
            json['ancillary_services'] = request_ancillary
            json['ownership'] = request_ownership
            json['activities'] = request_activities
            json['inpatient_service'] = request_inpatient
            json['staff'] = request_staff

            locality.set_geom(float(request_long), float(request_lat))
            locality.save()

            locality.set_values(json, request.user)
            return HttpResponse(request_uuid)

    else:
        print "not logged in"
    return HttpResponse('ERROR updating Locality and values')


def locality_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            request_lat = request.POST.get('lat')
            request_long = request.POST.get('long')
            request_name = request.POST.get('locality-name')
            request_physical_address = request.POST.get('physical-address')
            request_phone = request.POST.get('phone')
            request_operation = request.POST.get('operation')
            request_nature = request.POST.get('nature-of-facility')
            request_scope = request.POST.get('scope-of-service')
            request_ancillary = request.POST.get('ancillary')
            request_ownership = request.POST.get('ownership')
            request_activities = request.POST.get('activities')
            request_inpatient = request.POST.get('inpatient-service')
            request_staff = request.POST.get('staff')
            print request.POST

            tmp_changeset = Changeset.objects.create(
                social_user=request.user
            )

            # generate new uuid
            tmp_uuid = uuid.uuid4().hex

            loc = Locality()
            loc.changeset = tmp_changeset
            loc.domain = Domain.objects.get(name="Health")
            loc.uuid = tmp_uuid

            # generate unique upstream_id
            loc.upstream_id = u'web¶{}'.format(tmp_uuid)

            loc.geom = Point(
                float(request_long), float(request_lat)
            )
            loc.save()
            print loc

            json = {}
            json['name'] = request_name
            json['physical_address'] = request_physical_address
            json['phone'] = request_phone
            json['operation'] = request_operation
            json['nature_of_facility'] = request_nature
            json['scope_of_service'] = request_scope
            json['ancillary_services'] = request_ancillary
            json['ownership'] = request_ownership
            json['activities'] = request_activities
            json['inpatient_service'] = request_inpatient
            json['staff'] = request_staff

            loc.set_values(json, request.user)
            return HttpResponse(tmp_uuid)

    else:
        print "not logged in"
    return HttpResponse('ERROR updating Locality and values')


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

            # load_data_task.delay(data_loader.pk)

            response = {}
            success_message = 'You have successfully upload your data'
            # response['created'] = csv_importer.report['created']
            # response['modified'] = csv_importer.report['modified']
            # response['duplicated'] = csv_importer.report['duplicated']

            response['message'] = success_message
            response['success'] = True
            response['detailed_message'] = (
                'Please wait several minutes for Healthsites to load your data. We will send you an email if we '
                'have finished loading the data.'
            )
            # if response['duplicated'] > 0:
            #     response['detailed_message'] += (
            #         ' You also have %s possible duplicated localities, '
            #         'and they are not added.' % response['duplicated']
            #     )
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


class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        return super(SearchView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=google_maps_api_key)
        geoname = self.form_class.cleaned_data['id_search']
        LOG.info(geoname)
        geocode_result = gmaps.geocode(geoname)
        LOG.info(geocode_result)
        return reverse('search')


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
        result = []
        try:
            output = ""
            # locality which in polygon
            # data for frontend
            complete = 0
            partial = 0
            basic = 0
            northeast_lat = 0.0
            northeast_lng = 0.0
            southwest_lat = 0.0
            southwest_lng = 0.0
            if query != "":
                # getting viewport
                try:
                    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
                    gmaps = googlemaps.Client(key=google_maps_api_key)
                    geocode_result = gmaps.geocode(query)[0]
                    viewport = geocode_result['geometry']['viewport']
                    northeast_lat = viewport['northeast']['lat']
                    northeast_lng = viewport['northeast']['lng']
                    southwest_lat = viewport['southwest']['lat']
                    southwest_lng = viewport['southwest']['lng']
                except:
                    print "except"
                # getting country's polygon
                country = Country.objects.get(
                    name__iexact=query)
                polygons = country.polygon_geometry

                # query for each of attribute
                healthsites = Locality.objects.in_polygon(
                    polygons)
                healthsites_number = healthsites.count()
                filtered_value = Value.objects.filter(
                    locality__geom__within=polygons)
                hospital_number = filtered_value.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='hospital').count()
                medical_clinic_number = filtered_value.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='clinic').count()
                orthopaedic_clinic_number = filtered_value.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='orthopaedic clinic').count()
            else:
                # query for each of attribute
                healthsites = Locality.objects.all()
                healthsites_number = healthsites.count()
                hospital_number = Value.objects.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='hospital').count()
                medical_clinic_number = Value.objects.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='clinic').count()
                orthopaedic_clinic_number = Value.objects.filter(
                    specification__attribute__key='type').filter(
                    data__iexact='orthopaedic').count()

            # check completnees
            values = Value.objects.filter(locality__in=healthsites).exclude(data__isnull=True).exclude(
                data__exact='').values('locality').annotate(
                value_count=Count('locality'))
            # get attributes
            attribute_count = Attribute.objects.all().count() + 1  # geom
            # count completeness based attributes
            # this make long waiting, need to more good query
            complete = values.filter(value_count__gte=attribute_count).count()
            partial = values.filter(value_count__gte=4).filter(value_count__lte=attribute_count - 1).count()
            basic = values.filter(value_count__lte=3).count()

            output = {"numbers": {"hospital": hospital_number, "medical_clinic": medical_clinic_number
                , "orthopaedic_clinic": orthopaedic_clinic_number},
                      "completeness": {"complete": complete, "partial": partial, "basic": basic},
                      "localities": healthsites_number,
                      "viewport": {"northeast_lat": northeast_lat, "northeast_lng": northeast_lng,
                                   "southwest_lat": southwest_lat, "southwest_lng": southwest_lng}}

            result = json.dumps(output)
        except Country.DoesNotExist:
            result = []
            result = json.dumps(result)

        result = json.dumps(output)
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
