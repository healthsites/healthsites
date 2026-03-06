from api.utils import get_osm_schema

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from rest_framework.filters import BaseFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyTokenAuthScheme(OpenApiAuthenticationExtension):
    """Map APIKeyAuthentication to an OpenAPI tokenAuth security scheme."""

    target_class = 'api.api_views.v2.authentication.APIKeyAuthentication'
    name = 'tokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'Token',
            'description': 'Token-based authentication. Enter your API key.',
        }


def remove_cookie_auth(result, generator, request, public):
    """Postprocessing hook: remove cookieAuth from the generated schema."""
    schemes = result.get('components', {}).get('securitySchemes', {})
    schemes.pop('cookieAuth', None)
    security = result.get('security', [])
    result['security'] = [s for s in security if 'cookieAuth' not in s]
    return result


class Parameters(object):
    """ Class that holds all parameter schemas
    """
    api_key = {
        'name': 'api-key',
        'required': True,
        'in': 'query',
        'description': 'API KEY for accessing healthsites api.',
        'schema': {'type': 'string'},
    }

    page = {
        'name': 'page',
        'required': False,
        'in': 'query',
        'description': 'A page number within the paginated result set.',
        'schema': {'type': 'integer', 'default': 1},
    }

    extent = {
        'name': 'extent',
        'required': False,
        'in': 'query',
        'description': (
            'Extent of map that is used for filtering data. '
            '(format: minLng, minLat, maxLng, maxLat)'
        ),
        'schema': {'type': 'string'},
    }

    timestamp_from = {
        'name': 'from',
        'required': False,
        'in': 'query',
        'description': 'Get latest modified data from this timestamp.',
        'schema': {'type': 'integer'},
    }

    timestamp_to = {
        'name': 'to',
        'required': False,
        'in': 'query',
        'description': 'Get latest modified data from this timestamp.',
        'schema': {'type': 'integer'},
    }

    country = {
        'name': 'country',
        'required': False,
        'in': 'query',
        'description': 'Filter by country',
        'schema': {'type': 'string'},
    }

    output = {
        'name': 'output',
        'required': False,
        'in': 'query',
        'description': (
            'Output format for the request. '
            '(json/xml/geojson, default: json)'
        ),
        'schema': {'type': 'string'},
    }

    flat = {
        'name': 'flat-properties',
        'required': False,
        'in': 'query',
        'description': 'Put true to show properties in flat',
        'schema': {'type': 'string'},
    }

    tag_format = {
        'name': 'tag-format',
        'required': False,
        'in': 'query',
        'description': 'Tag format that want to be used. (osm/hxl. default : osm)',
        'schema': {'type': 'string'},
    }

    q = {
        'name': 'q',
        'required': True,
        'in': 'query',
        'description': 'Query that needs to be checked.',
        'schema': {'type': 'string'},
    }


def filter_api_key_endpoints(endpoints, **kwargs):
    """Preprocessing hook: only include endpoints using APIKeyAuthentication."""
    from api.api_views.v2.authentication import APIKeyAuthentication
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        cls = getattr(callback, 'cls', None)
        if cls and APIKeyAuthentication in getattr(
                cls, 'authentication_classes', []):
            filtered.append((path, path_regex, method, callback))
    return filtered


class ApiSchemaBaseWithoutApiKey(BaseFilterBackend):
    schemas = []

    def get_schema_operation_parameters(self, view):
        return self.schemas


class ApiSchemaBase(BaseFilterBackend):
    schemas = []

    def get_schema_operation_parameters(self, view):
        return [Parameters.api_key] + self.schemas


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
