# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '15/04/19'

from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView, Response
from localities_osm.serializer.locality_osm import LocalityOSMAutoCompleteSerializer
from localities_osm.queries import all_locality, filter_locality


class Autocomplete(APIView):
    def get(self, request):
        q = request.GET.get('q', '').capitalize()
        if len(q) > 2:
            if ' in ' in q:
                search_query = q.split(' in ')
                place = search_query[1]
                q = search_query[0]
                try:
                    query = filter_locality(place=place)
                except:  # noqa
                    query = all_locality()
            else:
                query = all_locality()

            search_qs = query.filter(name__icontains=q)
            serializer = \
                LocalityOSMAutoCompleteSerializer(search_qs, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseBadRequest('Insufficient characters.')
