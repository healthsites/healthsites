__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from localities_osm.models.locality import LocalityOSM


def convert_into_osm_dict(locality):
    """Utility to convert old locality dict into osm dict.

    :param locality: Locality object.
    :type locality: localities.models.Locality

    """

    data = locality.repr_dict()

    osm_dict = data['values']
    osm_dict['name'] = data['name']
    if osm_dict.get('physical_address', None):
        osm_dict['addr_full'] = osm_dict['physical_address']
        del osm_dict['physical_address']

    if osm_dict.get('phone', None):
        osm_dict['contact_number'] = osm_dict['phone']
        del osm_dict['phone']

    if osm_dict.get('staff', None):
        staff = osm_dict['staff'].split('|')

        if staff[0] is not u'':  # noqa
            osm_dict['staff_doctors'] = staff[0]

        try:
            if staff[1] is not u'':  # noqa
                osm_dict['staff_nurses'] = staff[1]
        except IndexError:
            pass

        del osm_dict['staff']

    if osm_dict.get('inpatient_service', None):
        beds = osm_dict['inpatient_service'].split('|')

        if beds[0] is not u'':  # noqa
            osm_dict['beds'] = beds[0]

        try:
            if beds[1] is not u'':  # noqa
                osm_dict['partial_beds'] = beds[1]
        except IndexError:
            pass

        del osm_dict['inpatient_service']

    for item, value in osm_dict.items():
        if '|' in value:
            value = value.split('|')
            osm_dict[item] = list(filter(None, value))

    return osm_dict


def split_osm_and_extension_attr(locality_attr):
    """Utility to split osm and extension attributes.

    :param locality_attr: Locality attributes.
    :type locality_attr: dict
        example: {
            "activities": [
                "medicine and medical specialties",
                "Maternal and women health",
                "pediatric care"
            ],
            "facility": "puskesmas",
            "notes": [
                "Outpatient consultation"
            ],
            "tags": [
                "general"
            ],
            "scope_of_service": [
                "specialized care",
                "general acute care",
                "rehabilitation care"
            ],
            "inpatient_service": "12",
            "staff_doctors": "8",
        }

    """

    osm_fields = [f.name for f in LocalityOSM._meta.get_fields()]

    osm_attr = {}
    for field in osm_fields:
        value = locality_attr.get(field, None)
        if (isinstance(value, bool) and value is not None) or value:
            osm_attr[field] = locality_attr[field]
        try:
            del locality_attr[field]
        except KeyError:
            pass

    if locality_attr.get('defining_hours', None):
        del locality_attr['defining_hours']

    return osm_attr, locality_attr
