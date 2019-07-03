__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'
from localities_osm_extension.models.extension import LocalityOSMExtension
from localities_osm_extension.models.tag import Tag


def save_extensions(osm_type, osm_id, extension):
    locality_extension, created = LocalityOSMExtension.objects.get_or_create(
        osm_id=osm_id,
        osm_type=osm_type
    )
    for item, value in extension.items():
        tag, created = Tag.objects.get_or_create(
            extension=locality_extension,
            name=item,
            value=value
        )
