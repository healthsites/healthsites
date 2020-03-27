from api.utils import get_osm_schema

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

import json
from core.settings.utils import ABS_PATH
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

    flat = Field(
        'flat-properties',
        location='query',
        required=False,
        schema=String(
            description='Put true to show properties in flat'
        ),
    )

    tag_format = Field(
        'tag-format',
        location='query',
        required=False,
        schema=String(
            description='Tag format that want to be used. (osm/hxl. default : osm)'
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


class Schema(object):
    def _change_type_into_string(self, type):
        if type == float:
            return 'float'
        elif type == str:
            return 'string'
        elif type == bool:
            return 'boolean'
        elif type == dict:
            return 'object'
        elif type == int:
            return 'integer'
        elif type == list:
            return 'list'
        return type

    def get_schema(self):
        schema = get_osm_schema()
        fields = schema['facilities']['create']['fields']
        for field in fields:
            field['type'] = self._change_type_into_string(field['type'])
            if field['key'] == 'tag':
                for tag in field['tags']:
                    tag['type'] = self._change_type_into_string(tag['type'])

        return schema


class SchemaView(APIView):
    def get(self, request):
        schema = Schema().get_schema()
        return Response(schema)
