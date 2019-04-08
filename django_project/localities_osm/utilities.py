__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '04/04/19'

from localities_osm.models.locality import LocalityOSMView


def get_all_osm_query():
    return LocalityOSMView.objects.filter(osm_id__isnull=False).exclude(name='')
