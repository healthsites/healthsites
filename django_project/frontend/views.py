# -*- coding: utf-8 -*-
import logging
import json

LOG = logging.getLogger(__name__)

from braces.views import FormMessagesMixin
from envelope.views import ContactView
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import googlemaps
from localities.views import search_locality_by_tag, get_country_statistic, search_locality_by_spec_data
from localities.models import Locality, Value, Country


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        context = super(MainView, self).get_context_data(**kwargs)

        context['debug'] = settings.DEBUG

        context['locality_count'] = Locality.objects.count()

        return context


class ContactView(FormMessagesMixin, ContactView):
    template_name = 'envelope/contact.html'
    form_invalid_message = 'There was an error in the contact form.'

    def get_form_valid_message(self):
        return u"{0} created!".format(self.object.title)


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


def search_place(request, place):
    # getting country's polygon
    result = {}
    result['locality_count'] = Locality.objects.count()
    result['countries'] = Country.objects.order_by('name').values('name').distinct()
    # geonames
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
        result['northeast_lat'] = "%f" % northeast_lat
        result['northeast_lng'] = "%f" % northeast_lng
        result['southwest_lat'] = "%f" % southwest_lat
        result['southwest_lng'] = "%f" % southwest_lng

    except:
        print "getting place error"
    return result


@csrf_exempt
def map(request):
    """View for request."""
    if request.method == 'POST':
        search_query = request.POST.get('q')
        option = request.POST.get('option')
        if option == 'place':
            map_url = reverse('map')
            return HttpResponseRedirect(
                    map_url + "?place=%s" % search_query)
        elif option == 'healthsite':
            locality_values = Value.objects.filter(
                    specification__attribute__key='name').filter(
                    data=search_query)
            if locality_values:
                locality_value = locality_values[0]
            else:
                locality_values = Value.objects.filter(
                        specification__attribute__key='name').filter(
                        data__istartswith=search_query)
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
                    map_url + "#!/locality/%s" % locality_uuid)
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
            result['polygon'] = Country.objects.get(name__iexact=country).polygon_geometry.geojson
        elif place:
            result = search_place(request, place)
        elif attribute:
            uuid = request.GET.get('uuid')
            result = search_locality_by_spec_data("attribute", attribute, uuid)
            result['attribute'] = {'attribute': attribute, 'uuid': uuid, 'name': result['locality_name']}
        elif len(request.GET) == 0:
            result = search_place(request, place)
        else:
            uuid = request.GET.get('uuid')
            print uuid
            for item in request.GET:
                if item != "uuid":
                    spec = item
                    data = request.GET.get(item)
                    result = search_locality_by_spec_data(spec, data, uuid)
                    result['spec'] = {'spec': spec, 'data': data, 'uuid': uuid, 'name': result['locality_name']}
        return render_to_response(
                'map.html',
                result,
                context_instance=RequestContext(request)
        )
