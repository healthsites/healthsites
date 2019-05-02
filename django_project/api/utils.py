# -*- coding: utf-8 -*-

import yaml

from os.path import exists

from api.osm_api_client import OsmApiWrapper
from core.settings.base import OSM_API_URL, APP_NAME
from core.settings.secret import SOCIAL_AUTH_OPENSTREETMAP_KEY, \
    SOCIAL_AUTH_OPENSTREETMAP_SECRET


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
