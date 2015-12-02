# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import googlemaps
from localities.models import Locality, Value


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


@csrf_exempt
def map(request):
    """View for request."""
    if request.method == 'POST':
        search_query = request.POST.get('q')
        option = request.POST.get('option')
        if option == 'place':
            # geonames
            google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
            gmaps = googlemaps.Client(key=google_maps_api_key)
            try:
                geocode_result = gmaps.geocode(search_query)[0]
                viewport = geocode_result['geometry']['viewport']
                northeast_lat = viewport['northeast']['lat']
                northeast_lng = viewport['northeast']['lng']
                southwest_lat = viewport['southwest']['lat']
                southwest_lng = viewport['southwest']['lng']
                request.session['tempe_bongkrek'] = 'alfonso'
                return render_to_response(
                    'map.html',
                    {
                        'northeast_lat': "%f" % northeast_lat,
                        'northeast_lng': "%f" % northeast_lng,
                        'southwest_lat': "%f" % southwest_lat,
                        'southwest_lng': "%f" % southwest_lng
                    },
                    context_instance=RequestContext(request)
                )
            except:
                return HttpResponseRedirect(reverse('map'))

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
        return render_to_response(
            'map.html',
            context_instance=RequestContext(request)
        )
