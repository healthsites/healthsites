# coding=utf-8
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

import requests
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
    try:
        params = {'q': geoname, 'format': 'json', 'limit': 1}
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params, headers={'Accept-Language': 'en'}
        )
        place = response.json()[0]
        viewport = place['boundingbox']
        northeast_lat = viewport[0]
        northeast_lng = viewport[2]
        southwest_lat = viewport[1]
        southwest_lng = viewport[3]
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
