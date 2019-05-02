# -*- coding: utf-8 -*-
from api.osm_api_client import OsmApiWrapper
from core.settings.base import OSM_API_URL


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


def changeset_tags(comment=None):
    """Helper to create osm changeset tags.

    :param comment: The changeset comment.
    :type comment: str

    :return: The changeset tags.
    :rtype: dict
    """
    tags = {}
    if comment:
        tags.update({
            'comment': comment
        })
    return tags


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
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=OSM_API_URL,
        appid='Healthsites.io'
    )
    osm_api.ChangesetCreate()
    changeset = osm_api.CreateNode(data)
    osm_api.ChangesetClose()

    return changeset
