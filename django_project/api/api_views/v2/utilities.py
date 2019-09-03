__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/02/19'

from localities_osm.utilities import split_osm_and_extension_attr
from localities_osm_extension.utils import save_extensions
from api.utils import (
    validate_osm_data,
    convert_to_osm_tag,
    create_osm_node
)
from api.utilities.pending import (
    create_pending_update,
    create_pending_review)
from core.settings.utils import ABS_PATH


class BadRequestError(Exception):
    def __init__(self, message):
        super(BadRequestError, self).__init__(message)


def create_osm_node_by_data(data, user, duplication_check=True):
    """ Create data based on data and user"""
    # Now, we post the data directly to OSM.
    try:
        # Split osm and extension attribute
        osm_attr, locality_attr = split_osm_and_extension_attr(
            data['tag'])
        data['tag'] = osm_attr

        validate_osm_data(data, duplication_check=duplication_check)

        # Map Healthsites tags to OSM tags
        mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
        data['tag'] = convert_to_osm_tag(
            mapping_file_path, data['tag'], 'node')

        # Push data to OSM
        response = create_osm_node(user, data)

        # create pending index
        create_pending_update(
            'node', response['id'],
            data['tag']['name'], user, response['version'])

        save_extensions('node', response['id'], locality_attr)
        return response

    except Exception as e:
        create_pending_review(user, data, '%s' % e)
        output = {
            'error': '%s' % e,
            'payload': data,
        }
        return output
