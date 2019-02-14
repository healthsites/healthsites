# -*- coding: utf-8 -*-
import logging
import os

import googlemaps
from envelope.views import ContactView
from hurry.filesize import size

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from braces.views import FormMessagesMixin

from localities.management.commands.generate_shapefile import directory_media
from localities.models import Country, DataLoaderPermission, Locality, Value
from localities.utils import (
    get_country_statistic, get_heathsites_master,
    search_locality_by_spec_data, search_locality_by_tag
)
from social_users.utils import get_profile

LOG = logging.getLogger(__name__)


class MainView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['debug'] = settings.DEBUG
        context['locality_count'] = get_heathsites_master().count()
        if request.user.is_authenticated():
            if request.user.is_staff:
                context['uploader'] = True
            else:
                permission = DataLoaderPermission.objects.filter(uploader=request.user)
                if len(permission) <= 0:
                    context['uploader'] = False
                else:
                    context['uploader'] = True
        else:
            context['uploader'] = False
        return self.render_to_response(context)


class ContactView(FormMessagesMixin, ContactView):
    template_name = 'envelope/contact.html'
    form_invalid_message = 'There was an error in the contact form.'

    def get_form_valid_message(self):
        return u'{0} created!'.format(self.object.title)


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        context = super(MapView, self).get_context_data(**kwargs)
        context['debug'] = settings.DEBUG
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class HelpView(TemplateView):
    template_name = 'help.html'


class AttributionsView(TemplateView):
    template_name = 'attributions.html'


def search_place(request, place):
    # getting country's polygon
    result = {}
    result['locality_count'] = get_heathsites_master().count()
    result['countries'] = Country.objects.order_by('name').values('name').distinct()
    # geonames
    if place:
        google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=google_maps_api_key)
        try:
            geocode_result = gmaps.geocode(place)[0]
            viewport = geocode_result['geometry']['viewport']
            northeast_lat = viewport['northeast']['lat']
            northeast_lng = viewport['northeast']['lng']
            southwest_lat = viewport['southwest']['lat']
            southwest_lng = viewport['southwest']['lng']
            request.session['tempe_bongkrek'] = 'alfonso'
            result['northeast_lat'] = '%f' % northeast_lat
            result['northeast_lng'] = '%f' % northeast_lng
            result['southwest_lat'] = '%f' % southwest_lat
            result['southwest_lng'] = '%f' % southwest_lng
        except Exception:
            print 'getting place error'
    return result


@csrf_exempt
def map(request):
    """View for request."""
    if request.user.is_authenticated():
        user = get_object_or_404(User, username=request.user)
        request.user = get_profile(user)

    if request.method == 'POST':
        search_query = request.POST.get('q')
        option = request.POST.get('option')
        if option == 'place':
            map_url = reverse('map')
            return HttpResponseRedirect(
                map_url + '?place=%s' % search_query)
        elif option == 'what3words':
            locality_values = Value.objects.filter(
                specification__attribute__key='what3words').filter(
                data=search_query)
            if locality_values:
                locality_value = locality_values[0]
            else:
                return render_to_response(
                    'map.html',
                    context_instance=RequestContext(request)
                )
            locality_uuid = locality_value.locality.uuid
            map_url = reverse('map')
            return HttpResponseRedirect(
                map_url + '#!/locality/%s' % locality_uuid)
        elif option == 'healthsite':
            localities = Locality.objects.filter(
                name=search_query)
            if len(localities) > 0:
                locality = localities[0]
                locality_uuid = locality.uuid
                map_url = reverse('map')
                return HttpResponseRedirect(
                    map_url + '#!/locality/%s' % locality_uuid)
            else:
                return render_to_response(
                    'map.html',
                    context_instance=RequestContext(request)
                )
    else:
        tag = request.GET.get('tag')
        country = request.GET.get('country')
        place = request.GET.get('place')
        attribute = request.GET.get('attribute')
        result = {}

        if tag:
            result = search_locality_by_tag(tag)
            result['tag'] = tag
        elif country:
            result = get_country_statistic(country)
            result['country'] = country
            result['polygon'] = (
                Country.objects.get(name__iexact=country).polygon_geometry.geojson
            )
            result['shapefile_size'] = 0
            filename = os.path.join(directory_media, country + '_shapefile.zip')
            if (os.path.isfile(filename)):
                result['shapefile_size'] = size(os.path.getsize(filename)) + 'B'
        elif place:
            result = search_place(request, place)
        elif attribute:
            uuid = request.GET.get('uuid')
            result = search_locality_by_spec_data('attribute', attribute, uuid)
            result['attribute'] = {
                'attribute': attribute, 'uuid': uuid, 'name': result['locality_name'],
                'location': result['location']
            }
        elif len(request.GET) == 0:
            result = search_place(request, place)
            # get facilities shapefile size
            result['shapefile_size'] = 0
            filename = os.path.join(directory_media, 'facilities_shapefile.zip')
            if (os.path.isfile(filename)):
                result['shapefile_size'] = size(os.path.getsize(filename)) + 'B'
        else:
            uuid = request.GET.get('uuid')
            for item in request.GET:
                if item != 'uuid':
                    spec = item
                    data = request.GET.get(item)
                    result = search_locality_by_spec_data(spec, data, uuid)
                    result['spec'] = {
                        'spec': spec, 'data': data, 'uuid': uuid,
                        'name': result['locality_name'], 'location': result['location']
                    }

        if 'new_geom' in request.session:
            result['new_geom'] = request.session['new_geom']
            del request.session['new_geom']
        return render_to_response(
            'map.html',
            result,
            context_instance=RequestContext(request)
        )
