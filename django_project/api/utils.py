# -*- coding: utf-8 -*-

import json
import yaml

from os.path import exists

from api import osm_tag_defintions
from api.osm_api_client import OsmApiWrapper
from api.osm_field_definitions import ALL_FIELDS
from api.osm_tag_defintions import get_mandatory_tags, update_tag_options
from core.settings.base import OSM_API_URL, APP_NAME
from core.settings.secret import SOCIAL_AUTH_OPENSTREETMAP_KEY, \
    SOCIAL_AUTH_OPENSTREETMAP_SECRET


def get_definition(keyword, definition_library, key=None):
    """Given a keyword and a key (optional), try to get a definition
    dict for it.

    :param keyword: A keyword key.
    :type keyword: str

    :param definition_library: A definition library/module.
    :type definition_library: module

    :param key: A specific key for a deeper search
    :type key: str

    :returns: A dictionary containing the matched key definition
        from definitions, otherwise None if no match was found.
    :rtype: dict, None
    """

    for item in dir(definition_library):
        if not item.startswith("__"):
            var = getattr(definition_library, item)
            if isinstance(var, dict):
                if var.get('key') == keyword or var.get(key) == keyword:
                    return dict(var)
    return None


def get_oauth_token(user):
    """Get OAuth token from social auth.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :return: The oauth_token and oauth_token_secret
    :rtype: tuple
    """
    social_auth = user.social_auth.get(provider='openstreetmap')
    access_token = social_auth.extra_data['access_token']
    return access_token['oauth_token'], access_token['oauth_token_secret']


def remap_dict(old_dict, transform):
    """
    Rename specific dictionary keys
    """
    new_dict = {}
    for k, v in old_dict.items():
        if k in transform:
            new_dict.update({transform[k]: v})
        else:
            new_dict.update({k: v})
    return new_dict


def convert_to_osm_tag(mapping_file_path, data, osm_type):
    """Convert local tags to osm tags based on mapping file.

    :param mapping_file_path: Path of the mapping file with yml format.
    :type mapping_file_path: str

    :param data: Locality data.
    :type data: dict

    :param osm_type: OSM geometry type of the data. 'node' or 'way'
    :type osm_type: str

    :return: Re-mapped locality data.
    :rtype: dict
    """
    if not exists(mapping_file_path):
        return data

    document = open(mapping_file_path, 'r')
    mapping_data = yaml.load(document)

    mapping_table_reference = 'healthcare_facilities_{}'.format(osm_type)
    mapping_data_reference = mapping_data.get(
        'tables', {}).get(mapping_table_reference, {})
    if not mapping_data_reference:
        return data

    # construct mapping dictionary
    mapping_dict = {}
    for column in mapping_data_reference.get('columns', []):
        try:
            mapping_dict.update({
                column['name']: column['key']
            })
        except:
            pass

    return remap_dict(data, mapping_dict)


def validate_osm_tags(osm_tags):
    """Validate osm tags using osm_tag_definitions.py as a reference.

    :param osm_tags: OSM tags.
    :type osm_tags: dict

    :return: Validation status and message.
    :rtype: tuple
    """

    message = 'OSM tags are valid.'

    # Mandatory tags check
    mandatory_tags = get_mandatory_tags(osm_tags)
    for mandatory_tag in mandatory_tags:
        if mandatory_tag['key'] not in osm_tags.keys():
            message = 'Invalid OSM tags: {} tag is missing.'.format(
                mandatory_tag['key'])
            return False, message

    # OSM tags value check
    for key, item in osm_tags.items():
        tag_definition = get_definition(key, osm_tag_defintions)
        tag_definition = update_tag_options(tag_definition, osm_tags)

        # Value type check
        if not isinstance(item, tag_definition.get('type')):
            message = (
                'Invalid value type for key {}: '
                'Expected type {}, got {} instead.').format(
                key, tag_definition['type'].__name__, type(item).__name__)
            return False, message

        # Value option check
        if tag_definition.get('options'):
            if item not in tag_definition.get('options'):
                message = (
                    'Invalid value for key {}: '
                    '{} is not a valid option.').format(key, item)
                return False, message

    return True, message


def create_osm_node(user, data):
    """Create OSM node data and push it to master OSM instance through OSM api.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :param data: OSM Node data.
    :type data: dict
        example: {
            'lat': latitude of node,
            'lon': longitude of node,
            'tag': {},
        }

    :return: OSM changeset data.
    :rtype: dict
        example: {
            'id': id of node,
            'lat': latitude of node,
            'lon': longitude of node,
            'tag': dict of tags,
            'changeset': id of changeset of last change,
            'version': version number of node,
            'user': username of last change,
            'uid': id of user of last change,
            'visible': True|False
        }
    """
    oauth_token, oauth_token_secret = get_oauth_token(user)
    osm_api = OsmApiWrapper(
        client_key=SOCIAL_AUTH_OPENSTREETMAP_KEY,
        client_secret=SOCIAL_AUTH_OPENSTREETMAP_SECRET,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=OSM_API_URL,
        appid=APP_NAME
    )
    response = osm_api.create_node(data)

    return response


def get_osm_schema():
    """Get schema based on osm tag definitions.

    :return: Defined OSM schema.
    :rtype: dict
    """
    with open('api/schema.json') as json_file:
        schema = json.load(json_file)
        schema['facilities']['create']['fields'] = ALL_FIELDS
        return schema
