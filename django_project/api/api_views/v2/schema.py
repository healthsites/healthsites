from api.utils import get_osm_schema

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from coreapi import Field
from coreschema import Integer, String
from rest_framework.filters import BaseFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response


class Parameters(object):
    """ Class that holds all parameter schemas
    """
    api_key = Field(
        'api-key',
        location='query',
        required=True,
        schema=String(
            description='API KEY for access healthsites api.'
        ),
    )

    page = Field(
        'page',
        location='query',
        required=True,
        schema=Integer(
            description='A page number within the paginated result set.'
        ),
    )

    extent = Field(
        'extent',
        location='query',
        required=False,
        schema=String(
            description='Extent of map that is used for filtering data. '
                        '(format: minLng, minLat, maxLng, maxLat)'
        ),
    )

    timestamp_from = Field(
        'from',
        location='query',
        required=False,
        schema=Integer(
            description='Get latest modified data from this timestamp.'
        ),
    )

    timestamp_to = Field(
        'to',
        location='query',
        required=False,
        schema=Integer(
            description='Get latest modified data from this timestamp.'
        ),
    )

    country = Field(
        'country',
        location='query',
        required=False,
        schema=String(
            description='Filter by country'
        ),
    )

    output = Field(
        'output',
        location='query',
        required=False,
        schema=String(
            description='Output format for the request. (json/xml/geojson, default: json)'
        ),
    )


class ApiSchemaBaseWithoutApiKey(BaseFilterBackend):
    schemas = []

    def get_schema_fields(self, view):
        schemas = self.schemas
        return schemas


class ApiSchemaBase(BaseFilterBackend):
    schemas = []

    def get_schema_fields(self, view):
        schemas = [Parameters.api_key] + self.schemas
        return schemas


class SchemaView(APIView):
    def get(self, request):
        schema = get_osm_schema()
        return Response(schema)
