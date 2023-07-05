# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/05/19'

from django.http.response import HttpResponseBadRequest
from rest_framework.views import APIView, Response

from api.api_views.v2.schema import (
    ApiSchemaBaseWithoutApiKey,
    Parameters
)
from api.serializer.country import CountryAutoCompleteSerializer
from localities.models import Country


class ApiSchema(ApiSchemaBaseWithoutApiKey):
    schemas = [Parameters.q]


class Autocomplete(APIView):
    filter_backends = (ApiSchema,)

    def get(self, request):
        q = request.GET.get('q', '').capitalize()
        if len(q) > 2:
            query = Country.objects.filter(name__icontains=q)
            serializer = \
                CountryAutoCompleteSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseBadRequest('Insufficient characters.')
