__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '04/04/19'

from localities_osm.models.locality import LocalityOSMView, LocalityOSM


def get_all_osm_query():
    return LocalityOSMView.objects.filter(osm_id__isnull=False).exclude(name='')


def convert_into_osm_dict(locality):
    data = locality.repr_dict()

    osm_dict = data['values']
    osm_dict['name'] = data['name']

    if 'staff' in osm_dict.keys():
        staff = osm_dict['staff'].split('|')
        osm_dict['staff_doctors'] = staff[0]
        osm_dict['staff_nurses'] = staff[1]
        del osm_dict['staff']

    if 'inpatient_service' in osm_dict.keys():
        beds = osm_dict['inpatient_service'].split('|')
        total_bed = int(beds[0]) + int(beds[1])
        osm_dict['inpatient_service'] = str(total_bed)

    for item, value in osm_dict.items():
        if '|' in value:
            value = value.split('|')
            osm_dict[item] = list(filter(None, value))

    return osm_dict


def split_osm_and_extension_attr(locality_attr):
    osm_fields = LocalityOSM._meta.get_all_field_names()

    osm_attr = {}
    for field in osm_fields:
        if field in locality_attr.keys():
            osm_attr[field] = locality_attr[field]
            del locality_attr[field]
        else:
            osm_attr[field] = ''

    if 'defining_hours' in locality_attr.keys():
        del locality_attr['defining_hours']

    return [osm_attr, locality_attr]
