__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from api.osm_tag_defintions import ALL_TAGS, MANDATORY_TAGS
from api.utils import get_osm_schema

_PYTHON_TYPE_TO_OPENAPI = {
    str: 'string',
    list: 'array',
    float: 'number',
    int: 'integer',
    bool: 'boolean',
    dict: 'object',
}


def _tag_to_property(tag):
    prop = {
        'type': _PYTHON_TYPE_TO_OPENAPI.get(tag['type'], 'string'),
        'description': tag.get('description', ''),
    }
    if 'options' in tag:
        prop['enum'] = tag['options']
    return prop


def _tag_example_value(tag):
    """Return a representative example value for a tag."""
    options = tag.get('options')
    python_type = tag['type']
    if options:
        return [options[0]] if python_type is list else options[0]
    if python_type is int:
        return 0
    if python_type is bool:
        return False
    if python_type is list:
        return []
    return ''


_TAG_EXAMPLE_OVERRIDES = {
    'name': 'Example Clinic',
    'operator': 'Ministry of Health',
    'contact_number': '+1-555-0100',
    'opening_hours': 'Mo-Fr 08:00-17:00',
    'beds': 50,
    'staff_doctors': 5,
    'staff_nurses': 20,
    'is_in_health_area': 'Health Area 1',
    'is_in_health_zone': 'Health Zone A',
    'url': 'https://example.com',
    'addr_housenumber': '123',
    'addr_street': 'Main Street',
    'addr_postcode': '12345',
    'addr_city': 'Example City',
}


class APIKeyTokenAuthScheme(OpenApiAuthenticationExtension):
    """Maps APIKeyAuthentication to an OpenAPI bearer security scheme.

    Swagger UI will prompt for the API key and automatically send it as
    'Authorization: Bearer <key>'.
    """

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
    """Postprocessing hook: remove cookieAuth and basicAuth from the generated schema."""
    schemes = result.get('components', {}).get('securitySchemes', {})
    schemes.pop('cookieAuth', None)
    schemes.pop('basicAuth', None)
    security = result.get('security', [])
    result['security'] = [
        s for s in security if 'cookieAuth' not in s and 'basicAuth' not in s
    ]
    return result


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


class Parameters(object):
    """Reusable OpenApiParameter definitions shared across API views."""

    api_key = OpenApiParameter(
        'api-key', str, OpenApiParameter.QUERY, required=False,
        description=(
            'API key for accessing the Healthsites API. '
            'Alternative to the Authorization: Bearer header.'
        ),
    )
    page = OpenApiParameter(
        'page', int, OpenApiParameter.QUERY, required=False,
        description='Page number within the paginated result set.',
        default=1,
    )
    extent = OpenApiParameter(
        'extent', str, OpenApiParameter.QUERY, required=False,
        description='Bounding box filter. '
                    'Format: minLng,minLat,maxLng,maxLat',
    )
    timestamp_from = OpenApiParameter(
        'from', int, OpenApiParameter.QUERY, required=False,
        description='Return facilities modified after this Unix timestamp.',
    )
    timestamp_to = OpenApiParameter(
        'to', int, OpenApiParameter.QUERY, required=False,
        description='Return facilities modified before this Unix timestamp.',
    )
    country = OpenApiParameter(
        'country', str, OpenApiParameter.QUERY, required=False,
        description='Filter results by country name.',
    )
    output = OpenApiParameter(
        'output', str, OpenApiParameter.QUERY, required=False,
        description='Response format.',
        enum=['json', 'xml', 'geojson'],
        default='json',
    )
    flat = OpenApiParameter(
        'flat-properties', str, OpenApiParameter.QUERY, required=False,
        description='Set to "true" to return properties in a flat structure.',
    )
    tag_format = OpenApiParameter(
        'tag-format', str, OpenApiParameter.QUERY, required=False,
        description='Tag format to use.',
        enum=['osm', 'hxl'],
        default='osm',
    )
    q = OpenApiParameter(
        'q', str, OpenApiParameter.QUERY, required=True,
        description='Query string to search.',
    )


class FacilityRequestSchema:
    """OpenAPI request body schema and examples for facility write operations."""

    create_request = {
        'application/json': {
            'type': 'object',
            'properties': {
                'lat': {'type': 'number', 'description': 'Latitude'},
                'lon': {'type': 'number', 'description': 'Longitude'},
                'tag': {
                    'type': 'object',
                    'description': 'OSM tags describing the facility.',
                    'properties': {
                        tag['key']: _tag_to_property(tag) for tag in ALL_TAGS
                    },
                    'required': [tag['key'] for tag in MANDATORY_TAGS],
                },
                'comment': {
                    'type': 'string',
                    'description': 'Changeset comment describing the edit.',
                },
                'source': {
                    'type': 'string',
                    'description': 'Source of the data (e.g. survey, imagery).',
                },
                'hashtags': {
                    'type': 'string',
                    'description': (
                        'Semicolon-separated changeset hashtags '
                        '(e.g. "#healthsites;#hotosm").'
                    ),
                },
            },
            'required': ['lat', 'lon', 'tag'],
        }
    }

    create_examples = [
        OpenApiExample(
            'Basic facility',
            value={
                'lat': 47.287,
                'lon': 8.765,
                'tag': {
                    tag['key']: _TAG_EXAMPLE_OVERRIDES.get(
                        tag['key'], _tag_example_value(tag)
                    )
                    for tag in ALL_TAGS
                },
            },
            request_only=True,
        ),
    ]


class ApiSchemaBaseWithoutApiKey(BaseFilterBackend):
    """Filter backend that exposes query parameters to the OpenAPI schema."""

    parameters = []

    def get_schema_operation_parameters(self, view):
        return self.parameters


class ApiSchemaBase(ApiSchemaBaseWithoutApiKey):
    """Filter backend that exposes query parameters including the API key."""

    def get_schema_operation_parameters(self, view):
        return [Parameters.api_key] + self.parameters


class Schema(object):
    """Converts the OSM schema field types to JSON-serialisable strings."""

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
    """Returns the OSM facility schema as JSON."""

    def get(self, request):
        schema = Schema().get_schema()
        return Response(schema)
