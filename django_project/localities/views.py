# -*- coding: utf-8 -*-
import logging
from django.core.serializers.json import DjangoJSONEncoder

LOG = logging.getLogger(__name__)

import googlemaps
import json
import uuid
# register signals
import signals  # noqa
from .forms import LocalityForm, DomainForm, DataLoaderForm, SearchForm
from .map_clustering import cluster
from .models import Locality, Domain, Changeset, Value, Attribute, Specification
from .models import LocalityArchive, ValueArchive
from .utils import render_fragment, parse_bbox
from braces.views import JSONResponseMixin, LoginRequiredMixin
from datetime import datetime
import time
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count, Max
from django.http import HttpResponse, Http404
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from localities.models import Country, DataLoader


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
            'bbox', 'zoom', 'iconsize', 'geoname', 'tag', 'spec', 'data'])):
            raise Http404

        try:
            bbox_poly = parse_bbox(request.GET.get('bbox'))
            zoom = int(request.GET.get('zoom'))
            icon_size = map(int, request.GET.get('iconsize').split(','))
            geoname = request.GET.get('geoname')
            tag = request.GET.get('tag')
            spec = request.GET.get('spec')
            data = request.GET.get('data')

        except:
            # return 404 if any of parameters are missing or not parsable
            raise Http404

        if zoom < 0 or zoom > 20:
            # zoom should be between 0 and 20
            raise Http404
        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise Http404

        return (bbox_poly, zoom, icon_size, geoname, tag, spec, data)

    def get(self, request, *args, **kwargs):
        # parse request params
        bbox, zoom, iconsize, geoname, tag, spec, data = self._parse_request_params(request)
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
                        localities = Value.objects.filter(
                                specification__attribute__key=spec).filter(
                                data__icontains=data).values('locality')
                        print localities
                        localities = Locality.objects.filter(id__in=localities)
        object_list = []
        if not exception:
            object_list = cluster(localities, zoom, *iconsize)
        print object_list
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
        attribute_count = 18
        # count completeness based attributes
        obj_repr = self.object.repr_dict()
        data_repr = render_fragment(
                self.object.domain.template_fragment, obj_repr
        )
        obj_repr.update({'repr': data_repr})

        num_data = len(obj_repr['values']) + 1  # geom
        completeness = (num_data + 0.0) / (attribute_count + 0.0) * 100  # percentage
        obj_repr.update({'completeness': '%s%%' % format(completeness, '.2f')})

        # get latest update
        try:
            updates = []
            last_updates = locality_updates(self.object.id, datetime.now())
            for last_update in last_updates:
                updates.append({"last_update": last_update['changeset__created'],
                                "uploader": last_update['changeset__social_user__username'],
                                "changeset_id": last_update['changeset']});
            obj_repr.update({'updates': updates})
        except Exception as e:
            print e

        # FOR HISTORY
        obj_repr['history'] = False
        if kwargs.has_key("changes"):
            changes = kwargs['changes']
            changeset = Changeset.objects.get(id=changes)
            obj_repr['updates'][0]['last_update'] = changeset.created
            obj_repr['updates'][0]['uploader'] = changeset.social_user.username
            obj_repr['updates'][0]['changeset_id'] = changes
            try:
                localityArchives = LocalityArchive.objects.filter(changeset=changes).filter(uuid=obj_repr['uuid'])
                for archive in localityArchives:
                    obj_repr['geom'] = (archive.geom.x, archive.geom.y)
                    obj_repr['history'] = True
            except LocalityArchive.DoesNotExist:
                print "next"

            try:
                localityArchives = ValueArchive.objects.filter(changeset=changes).filter(locality_id=self.object.id)
                for archive in localityArchives:
                    try:
                        specification = Specification.objects.get(id=archive.specification_id)
                        obj_repr['values'][specification.attribute.key] = archive.data
                        obj_repr['history'] = True
                    except Specification.DoesNotExist:
                        print "next"
            except LocalityArchive.DoesNotExist:
                print "next"
        print obj_repr

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


def locality_edit(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] == True:
                locality = Locality.objects.get(uuid=json_request['uuid'])
                locality.set_geom(float(json_request['long']), float(json_request['lat']))
                # there are some changes so create a new changeset
                tmp_changeset = Changeset.objects.create(
                        social_user=request.user
                )
                locality.changeset = tmp_changeset
                locality.save()
                locality.set_values(json_request, request.user, tmp_changeset)

                return HttpResponse(json.dumps(
                        {"valid": json_request['is_valid'], "uuid": json_request['uuid']}))
            else:
                return HttpResponse(
                        json.dumps({"valid": json_request['is_valid'], "key": json_request['invalid_key']}))

    else:
        print "not logged in"
    return HttpResponse('ERROR updating Locality and values')


def locality_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] == True:
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
                        float(json_request['long']), float(json_request['lat'])
                )
                loc.save()
                loc.set_values(json_request, request.user, tmp_changeset)

                return HttpResponse(json.dumps(
                        {"valid": json_request['is_valid'], "uuid": tmp_uuid}))
            else:
                return HttpResponse(
                        json.dumps({"valid": json_request['is_valid'], "key": json_request['invalid_key']}))

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


def get_statistic(healthsites):
    # locality which in polygon
    # data for frontend
    complete = 0
    partial = 0
    basic = 0

    healthsites_number = healthsites.count()
    values = Value.objects.filter(locality__in=healthsites)

    hospital_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='hospital').count()
    medical_clinic_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='clinic').count()
    orthopaedic_clinic_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='orthopaedic').count()

    # check completnees
    values = Value.objects.filter(locality__in=healthsites).exclude(data__isnull=True).exclude(
            data__exact='').values('locality').annotate(
            value_count=Count('locality'))
    # get attributes
    attribute_count = 18
    # count completeness based attributes
    # this make long waiting, need to more good query
    complete = values.filter(value_count__gte=attribute_count).count()
    partial = values.filter(value_count__gte=4).filter(value_count__lte=attribute_count - 1).count()
    basic = values.filter(value_count__lte=3).count()

    output = {"numbers": {"hospital": hospital_number, "medical_clinic": medical_clinic_number
        , "orthopaedic_clinic": orthopaedic_clinic_number},
              "completeness": {"complete": complete, "partial": partial, "basic": basic},
              "localities": healthsites_number}
    # updates
    last_updates = []
    histories = localities_updates(healthsites)
    for update in histories:
        update['locality_uuid'] = ""
        update['locality'] = ""
        if update['edit_count'] == 1:
            # get the locality to show in web
            try:
                locality = Locality.objects.get(pk=update['locality_id'])
                locality_name = Value.objects.filter(locality=locality).filter(
                        specification__attribute__key='name')
                update['locality_uuid'] = locality.uuid
                update['locality'] = locality_name[0].data
            except Locality.DoesNotExist:
                update['locality_uuid'] = "unknown"
                update['locality'] = "unknown"

        if 'version' in update:
            if update['version'] == 1:
                update['mode'] = 1
            else:
                update['mode'] = 2
        else:
            update['mode'] = 1

        last_updates.append({"author": update['changeset__social_user__username'],
                             "date_applied": update['changeset__created'],
                             "mode": update['mode'],
                             "locality": update['locality'],
                             "locality_uuid": update['locality_uuid'],
                             "data_count": update['edit_count']})
    output["last_update"] = last_updates;
    return output


def search_locality_by_tag(query):
    try:
        localities = Value.objects.filter(
                specification__attribute__key='tags').filter(data__icontains="|" + query + "|").values('locality')
        return get_statistic(localities)
    except Value.DoesNotExist:
        return []


def search_locality_by_spec_data(spec, data):
    try:
        localities = Value.objects.filter(
                specification__attribute__key=spec).filter(
                data__icontains=data).values('locality')
        return get_statistic(localities)
    except Value.DoesNotExist:
        return []


def get_country_statistic(query):
    output = ""
    try:
        if query != "":
            # getting country's polygon
            country = Country.objects.get(
                    name__iexact=query)
            polygons = country.polygon_geometry

            # query for each of attribute
            healthsites = Locality.objects.in_polygon(
                    polygons)
            output = get_statistic(healthsites)
        else:
            # query for each of attribute
            healthsites = Locality.objects.all()
            output = get_statistic(healthsites)
    except Country.DoesNotExist:
        output = ""
    return output


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


def get_simple_statistic_by_country(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        result = []
        try:
            output = {}
            # getting country's polygon
            country = Country.objects.get(
                    name__iexact=query)
            polygons = country.polygon_geometry

            # query for each of attribute
            healthsites = Locality.objects.in_polygon(
                    polygons)
            output['number'] = healthsites.count()

            # check completnees
            values = Value.objects.filter(locality__in=healthsites).values('locality').annotate(
                    value_count=Count('locality'))
            # 16 = 4 mandatory + 12 core
            # this make long waiting, need to more good query
            complete = values.filter(value_count__gte=15).count()
            if values.count() > 0:
                complete = complete * 100.0 / values.count()
            else:
                complete = 0.0
            output['completeness'] = "%.2f" % complete

            result = json.dumps(output)
        except Country.DoesNotExist:
            result = []
            result = json.dumps(result)

        result = json.dumps(output)
        return HttpResponse(result, content_type='application/json')


def get_locality_update(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        uuid = request.GET.get('uuid')
        if date == "":
            date = datetime.datetime.now()
        locality = Locality.objects.get(uuid=uuid)
        last_updates = locality_updates(locality.id, date)
        output = []
        for last_update in last_updates:
            output.append({"last_update": last_update['changeset__created'],
                           "uploader": last_update['changeset__social_user__username'],
                           "changeset_id": last_update['changeset']});
        result = json.dumps(output, cls=DjangoJSONEncoder)

    return HttpResponse(result, content_type='application/json')


def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(time.mktime(json['changeset__created'].timetuple()))
    except KeyError:
        return 0


def locality_updates(locality_id, date):
    updates = []
    try:
        updates1 = LocalityArchive.objects.filter(object_id=locality_id).filter(changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
                edit_count=Count('changeset'))[:15]
        for update in updates1:
            updates.append(update)
        updates2 = ValueArchive.objects.filter(locality_id=locality_id).filter(
                changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
                edit_count=Count('changeset'))[:15]
        for update in updates2:
            updates.append(update)
        updates.sort(key=extract_time, reverse=True)
    except LocalityArchive.DoesNotExist:
        print "Locality Archive not exist"

    output = []
    prev_changeset = 0
    for update in updates:
        if prev_changeset != update['changeset']:
            output.append(update)
        prev_changeset = update['changeset']
    return output[:10]


def localities_updates(locality_ids):
    updates = []
    try:
        updates1 = LocalityArchive.objects.filter(object_id__in=locality_ids).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('object_id'))[:15]
        for update in updates1:
            updates.append(update)
        updates2 = ValueArchive.objects.filter(locality_id__in=locality_ids).filter(version__gt=1).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('locality_id'))[:15]
        for update in updates2:
            updates.append(update)
        updates.sort(key=extract_time, reverse=True)
    except LocalityArchive.DoesNotExist:
        print "Locality Archive not exist"

    output = []
    prev_changeset = 0
    for update in updates:
        if prev_changeset != update['changeset']:
            output.append(update)
        prev_changeset = update['changeset']
    return output[:10]
