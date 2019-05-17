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
    'key': 'long',
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

ALL_FIELDS = [latitude, longitude, tag]
