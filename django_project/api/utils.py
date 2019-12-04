# -*- coding: utf-8 -*-

import json
import overpass
import yaml

from os.path import exists
from social_django.models import UserSocialAuth
from api import osm_tag_defintions
from api.osm_api_client import OsmApiWrapper
from api.osm_field_definitions import ALL_FIELDS, get_mandatory_fields
from api.osm_tag_defintions import get_mandatory_tags, update_tag_options
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.settings.utils import ABS_PATH
from social_users.models import TrustedUser, Organisation


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
        if not item.startswith('__'):
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
    try:
        social_auth = user.social_auth.get(provider='openstreetmap')
        access_token = social_auth.extra_data['access_token']
        return access_token['oauth_token'], access_token['oauth_token_secret']
    except UserSocialAuth.DoesNotExist:
        raise Exception('This user is not linked to openstreetmap yet')


def is_organizer(user):
    """Check whether the user is an organizer or not.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :return: Boolean indicator
    :rtype: bool
    """
    try:
        return len(Organisation.objects.filter(organizer=user)) > 0
    except Organisation.DoesNotExist:
        return False


def is_trusted_user(user):
    """Check whether the user is a trusted user or not.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :return: Boolean indicator
    :rtype: bool
    """
    try:
        return len(TrustedUser.objects.filter(user=user)) > 0
    except TrustedUser.DoesNotExist:
        return False


def remap_dict(old_dict, transform):
    """
    Rename specific dictionary keys
    """
    new_dict = {}
    for k, v in old_dict.items():
        try:
            v = v.decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
            pass

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
    mapping_data = yaml.load(document, Loader=yaml.BaseLoader)

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
            if isinstance(data[column['name']], bool):
                data[column['name']] = 'True' if data[column['name']] else 'False'
            elif isinstance(data[column['name']], int) \
                    or isinstance(data[column['name']], float):
                data[column['name']] = '%s' % data[column['name']]
            elif isinstance(data[column['name']], list):
                data[column['name']] = '%s' % ';'.join(data[column['name']])
        except:  # noqa
            pass

    return remap_dict(data, mapping_dict)


def validate_osm_data(osm_data, duplication_check=True):
    """Validate osm data based on osm field and tag definition.

    :param data_owner: The owner of the data.
    :type data_owner: django.contrib.auth.models.User

    :param osm_data: OSM data.
    :type osm_data: dict

    :param duplication_check: Flag indicating to use duplication validation.
    :type duplication_check: bool

    :return: Validation status and message.
    :rtype: tuple
    """
    try:
        osm_data['tag']['source'] = 'healthsites.io'
    except KeyError:
        pass

    # Validate fields
    is_valid, message = validate_osm_fields(osm_data)
    if not is_valid:
        raise Exception(message)

    # Validate tags
    is_valid, message = validate_osm_tags(osm_data.get('tag', {}))
    if not is_valid:
        raise Exception(message)

    if duplication_check:
        # Validate duplication
        is_valid, message = validate_duplication(osm_data)
        if not is_valid:
            raise Exception(message)

    return True


def verify_user(uploader, creator, ignore_uploader_staff=False):
    """Verify user.

    Uploader has to be organizer of an organisation and the creator has to be
    a trusted user in that particular organisation.

    :param uploader: The data uploader
    :type uploader: str or User object

    :param creator: The data creator/owner
    :type creator: str or User object

    :return: Verification status and message.
    :rtype: tuple
    """
    uploader = get_object_or_404(User, username=uploader)
    if uploader.is_staff and not ignore_uploader_staff:
        return True, (
            'Data uploader is staff.')

    try:
        organisation = get_object_or_404(Organisation, organizer=uploader)
    except Http404:
        return False, 'User %s is not organizer of an organisation.' % uploader

    try:
        creator = get_object_or_404(User, username=creator)
        if creator not in (
                [trusted_user.user for trusted_user in TrustedUser.objects.filter(
                    organisation=organisation)]):
            return False, 'User %s is not a trusted user.' % creator
    except Http404:
        return False, 'User %s is not exist.' % creator

    return True, (
        'Data uploader is an organizer and creator/owner is a trusted user.')


def validate_osm_fields(osm_fields):
    """Validate osm fields using osm_field_definitions.py as a reference.

    :param osm_fields: OSM fields.
    :type osm_fields: dict

    :return: Validation status and message.
    :rtype: tuple
    """
    # Mandatory fields check
    mandatory_fields = get_mandatory_fields(osm_fields)
    for mandatory_field in mandatory_fields:
        if mandatory_field['key'] not in osm_fields.keys():
            message = 'Invalid OSM fields: {} field is missing.'.format(
                mandatory_field['key'])
            return False, message

    return True, 'OSM fields are valid.'


def validate_osm_tags(osm_tags):
    """Validate osm tags using osm_tag_definitions.py as a reference.

    :param osm_tags: OSM tags.
    :type osm_tags: dict

    :return: Validation status and message.
    :rtype: tuple
    """
    # Mandatory tags check
    mandatory_tags = get_mandatory_tags(osm_tags)
    for mandatory_tag in mandatory_tags:
        if mandatory_tag['key'] not in osm_tags.keys():
            message = 'Invalid OSM tags: `{}` tag is missing.'.format(
                mandatory_tag['key'])
            return False, message

    # OSM tags value check
    for key, item in osm_tags.items():
        tag_definition = get_definition(key, osm_tag_defintions)
        if not tag_definition:
            continue
        tag_definition = update_tag_options(tag_definition, osm_tags)

        # Value type check
        if tag_definition.get('type') == 'string':
            tag_definition['type'] = str
        elif tag_definition.get('type') == 'integer':
            tag_definition['type'] = int
        elif tag_definition.get('type') == 'float':
            tag_definition['type'] = float
        elif tag_definition.get('type') == 'boolean':
            tag_definition['type'] = bool
        elif tag_definition.get('type') == 'list':
            tag_definition['type'] = list

        if tag_definition.get('type') == str:
            if not isinstance(item, unicode):
                item = str(item)
        elif tag_definition.get('type') == int:
            item = int(item)
        elif tag_definition.get('type') == bool:
            if item == 'False':
                item = False
            elif item == 'True':
                item = True
        if tag_definition['type'] == list:
            if not isinstance(item, list):
                item = [item]
        if not isinstance(item, tag_definition.get('type')):
            if not (isinstance(item, unicode) and tag_definition.get('type') == str):
                message = (
                    'Invalid value type for key `{}`: '
                    'Expected type `{}`, got `{}` instead.').format(
                    key, tag_definition['type'].__name__, type(item).__name__)
                return False, message

        # Value option check
        if tag_definition.get('options'):
            current_item = item
            if not isinstance(current_item, list):
                current_item = [current_item]
            for row in current_item:
                if row not in tag_definition.get('options'):
                    message = (
                        'Invalid value for key `{}`: '
                        '`{}` is not a valid option.').format(key, row)
                    return False, message

    return True, 'OSM tags are valid.'


def validate_duplication(osm_data):
    """Validate if given osm data is already exist in osm instance.

    :param osm_data: OSM data.
    :type osm_data: dict

    :return: Validation status and message.
    :rtype: tuple
    """
    # We need to determine several scenarios for validating the duplication.
    # At first, we will use Overpass QL to check whether node with given name
    # is exist in the bounding box.

    # create bounding box with delta = 0.001
    radius = settings.DUPLICATION_RADIUS
    lon = osm_data['lon']
    lat = osm_data['lat']

    op_api = overpass.API()
    name = osm_data['tag']['name']
    query = (
        u'('
        u'node["name"="{name}"](around:{radius}, {lat}, {lon});'
        u'node["name:en"="{name}"](around:{radius}, {lat}, {lon});'
        ')'.format(
            name=name,
            radius=radius,
            lon=lon,
            lat=lat))
    response = op_api.get(query.encode('utf-8'))
    if len(response.get('features', [])) > 0:
        message = 'Duplication detected. Records = %s' % [
            feature['id'] for feature in response.get('features')]
        return False, message

    return True, 'No duplication found.'


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
        client_key=settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
        client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=settings.OSM_API_URL,
        appid=settings.APP_NAME
    )
    response = osm_api.create_node(data)

    return response


def update_osm_node(user, data):
    """Update OSM node data and push it to master OSM instance through OSM api.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :param data: OSM Node data.
    :type data: dict
        example: {
            'id': id of node,
            'lat': latitude of node,
            'lon': longitude of node,
            'tag': {},
            'version': version number of node,
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
        client_key=settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
        client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=settings.OSM_API_URL,
        appid=settings.APP_NAME
    )
    response = osm_api.update_node(data)

    return response


def delete_osm_node(user, data):
    """Delete OSM node data through OSM api.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :param data: OSM Node data.
    :type data: dict
        example: {
            'id': id of node,
            'lat': latitude of node,
            'lon': longitude of node,
            'version': version number of node,
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
        client_key=settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
        client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=settings.OSM_API_URL,
        appid=settings.APP_NAME
    )
    response = osm_api.delete_node(data)

    return response


def update_osm_way(user, data):
    """Update OSM way data and push it to master OSM instance through OSM api.

    :param user: The user.
    :type user: django.contrib.auth.models.User

    :param data: OSM Way data.
    :type data: dict
        example: {
            'id': id of node,
            'tag': {},
            'version': version number of node,
        }

    :return: OSM changeset data.
    :rtype: dict
        example: {
            'id': id of node,
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
        client_key=settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
        client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        api=settings.OSM_API_URL,
        appid=settings.APP_NAME
    )
    response = osm_api.update_way(data)

    return response


def get_osm_schema():
    """Get schema based on osm tag definitions.

    :return: Defined OSM schema.
    :rtype: dict
    """
    schema_template_file_path = ABS_PATH('api', 'fixtures', 'schema.json')
    with open(schema_template_file_path) as json_file:
        schema = json.load(json_file)
        schema['facilities']['create']['fields'] = ALL_FIELDS
        return schema
