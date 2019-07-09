# -*- coding: utf-8 -*-

# OSM fields definition
from api.osm_tag_defintions import ALL_TAGS

latitude = {
    'key': 'lat',
    'name': 'latitude',
    'description': 'Latitude position of the healthsite.',
    'required': True,
    'type': float
}

longitude = {
    'key': 'lon',
    'name': 'longitude',
    'description': 'Longitude position of the healthsite.',
    'required': True,
    'type': float
}

tag = {
    'key': 'tag',
    'name': 'tag',
    'description': 'OSM tags.',
    'required': True,
    'type': dict,
    'tags': ALL_TAGS
}

osm_user = {
    'key': 'osm_user',
    'name': 'osm_user',
    'description': 'Username of an OSM account.',
    'required': True,
    'type': float
}

ALL_FIELDS = [latitude, longitude, tag]

MANDATORY_FIELDS = [field for field in ALL_FIELDS if field.get('required')]


def get_mandatory_fields(osm_fields):
    """Get special mandatory fields based on requested osm data.

    :param osm_fields: OSM tags.
    :type osm_fields: dict

    :return: List of mandatory tags.
    :rtype: list
    """
    # Please define custom rule here if any.

    return MANDATORY_FIELDS
