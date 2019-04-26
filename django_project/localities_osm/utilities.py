__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '04/04/19'

from localities_osm.models.locality import LocalityOSMView, LocalityOSM


def get_all_osm_query():
    return LocalityOSMView.objects.filter(osm_id__isnull=False).exclude(name='')


def convert_into_osm_dict(locality):
    """Utility to convert old locality dict into osm dict."""

    data = locality.repr_dict()

    osm_dict = data['values']
    osm_dict['name'] = data['name']

    if osm_dict.get('staff', None):
        staff = osm_dict['staff'].split('|')
        staff = [u'0' if v is u'' else v for v in staff]
        osm_dict['staff_doctors'] = staff[0]
        osm_dict['staff_nurses'] = staff[1]
        del osm_dict['staff']

    if osm_dict.get('inpatient_service', None):
        beds = osm_dict['inpatient_service'].split('|')
        beds = list(filter(None, beds))
        beds = [int(x) for x in beds]
        total_bed = sum(beds)
        osm_dict['inpatient_service'] = str(total_bed)

    if not osm_dict.get('inpatient_service', None):
        osm_dict['inpatient_service'] = '0'

    for item, value in osm_dict.items():
        if '|' in value:
            value = value.split('|')
            osm_dict[item] = list(filter(None, value))

    return osm_dict


def split_osm_and_extension_attr(locality_attr):
    """Utility to split osm and extension attributes."""

    osm_fields = LocalityOSM._meta.get_all_field_names()

    osm_attr = {}
    for field in osm_fields:
        if locality_attr.get(field, None):
            osm_attr[field] = locality_attr[field]
            del locality_attr[field]
        else:
            osm_attr[field] = ''

    if locality_attr.get('defining_hours', None):
        del locality_attr['defining_hours']

    return osm_attr, locality_attr
