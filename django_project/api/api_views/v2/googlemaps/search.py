# coding=utf-8
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

import googlemaps
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView, Response

from api.api_views.v2.schema import Parameters


def search_by_geoname(geoname):
    """ Return location based on geoname

    :param geoname: geoname query that will be searched
    :type geoname: str
    :return: {
        'northeast': {
            'lat': '%f' % northeast_lat,
            'lng': '%f' % northeast_lng,
        },
        'southwest': {
            'lat': '%f' % southwest_lat,
            'lng': '%f' % southwest_lng,
        }
    }

    """
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    gmaps = googlemaps.Client(key=google_maps_api_key)
    try:
        geocode_result = gmaps.geocode(geoname)[0]
        viewport = geocode_result['geometry']['viewport']
        northeast_lat = viewport['northeast']['lat']
        northeast_lng = viewport['northeast']['lng']
        southwest_lat = viewport['southwest']['lat']
        southwest_lng = viewport['southwest']['lng']
        return {
            'northeast': {
                'lat': northeast_lat,
                'lng': northeast_lng,
            },
            'southwest': {
                'lat': southwest_lat,
                'lng': southwest_lng,
            }
        }
    except IndexError:
        raise Exception('place is not found')


class SearchByGeoname(APIView):
    """
    Search Location using geoname as query (q)
    """
    exclude_from_docs = True
    schema = AutoSchema(manual_fields=[
        Parameters.q
    ])

    def get(self, request):
        q = request.GET.get('q', '')
        if len(q) > 2:
            try:
                return Response(search_by_geoname(q))
            except Exception as e:
                return HttpResponseBadRequest('%s' % e)
        else:
            return HttpResponseBadRequest('Insufficient characters.')
