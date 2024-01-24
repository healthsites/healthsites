__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from localities_osm_extension.models.extension import LocalityOSMExtension
from localities_osm_extension.models.tag import Tag


def save_extensions(osm_type, osm_id, extension):
    """
    Save the extensions
    """
    locality_extension, created = LocalityOSMExtension.objects.get_or_create(
        osm_id=osm_id,
        osm_type=osm_type
    )
    for item, value in extension.items():
        if value:
            if isinstance(value, list):
                value = ';'.join(value)
            value = '%s' % value
            Tag.objects.get_or_create(
                extension=locality_extension,
                name=item,
                value=value
            )
