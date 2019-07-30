# -*- coding: utf-8 -*-

# Healthsites related tags

# Mandatory tags - see https://github.com/healthsites/healthsites/issues/1129


amenity = {
    'key': 'amenity',
    'name': 'amenity',
    'description':
        'For describing useful and important facilities '
        'for visitors and residents',
    'options': [
        'clinic', 'doctors', 'hospital', 'dentist', 'pharmacy'
    ],
    'required': True,
    'type': str,
}

healthcare = {
    'key': 'healthcare',
    'name': 'healthcare',
    'description':
        'A key to tag all places that provide healthcare '
        '(are part of the healthcare sector)',
    'options': [
        'doctor', 'pharmacy', 'hospital', 'clinic', 'dentist',
        'physiotherapist', 'alternative', 'laboratory', 'optometrist',
        'rehabilitation', 'blood_donation', 'birthing_center'
    ],
    'required': True,
    'type': list,
}

name = {
    'key': 'name',
    'name': 'name',
    'description': 'Name for buildings and facilities',
    'required': True,
    'type': str,
}

operator = {
    'key': 'operator',
    'name': 'operator',
    'description':
        'The operator tag is used to name a company, corporation, '
        'person or any other entity who is directly in charge of '
        'the current operation of a map object',
    'required': True,
    'type': str,
}

source = {
    'key': 'source',
    'name': 'source',
    'description':
        'Used to indicate the source of information '
        '(i.e. meta data) added to OpenStreetMap',
    'required': True,
    'type': str,
}

# Not mandatory tags
speciality = {
    'key': 'speciality',
    'name': 'speciality',
    'description':
        'A key to detail the special services provided by '
        'a healthcare facility. '
        'To be used in conjuction with the \'healthcare=*\' tag. '  # noqa
        'For example \'healthcare=laboratory\', '  # noqa
        'and \'healthcare:speciality=blood_check\'',  # noqa
    'options': [],
    'required': False,
    'type': list,
}

operator_type = {
    'key': 'operator_type',
    'name': 'operator_type',
    'description':
        'This tag is used to give more information about '
        'the type of operator for a feature',
    'options': [
        'public', 'private', 'community', 'religious', 'government', 'ngo',
        'combination'
    ],
    'required': False,
    'type': str,
}

addr_full = {
    'key': 'addr_full',
    'name': 'addr_full',
    'description':
        'Address for buildings and facilities',
    'required': False,
    'type': str,
}

contact_number = {
    'key': 'contact_number',
    'name': 'contact_number',
    'description':
        'Contact number of facility',
    'required': False,
    'type': str,
}

operational_status = {
    'key': 'operational_status',
    'name': 'operational_status',
    'description':
        'Used to document an observation of the current '
        'functional status of a mapped feature',
    'options': [
        'operational', 'non_operational', 'unknown'
    ],
    'required': False,
    'type': str,
}

opening_hours = {
    'key': 'opening_hours',
    'name': 'opening_hours',
    'description':
        'Time of facility open',
    'required': False,
    'type': str,
}

beds = {
    'key': 'beds',
    'name': 'beds',
    'description': 'Indicates the number of beds in a hotel or hospital',
    'required': False,
    'type': int,
}

staff_doctors = {
    'key': 'staff_doctors',
    'name': 'staff_doctors',
    'description': 'Indicates the number of doctors in a hospitall',
    'required': False,
    'type': int,
}

staff_nurses = {
    'key': 'staff_nurses',
    'name': 'staff_nurses',
    'description': 'Indicates the number of nurses in a hospitall',
    'required': False,
    'type': int,
}

health_amenity_type = {
    'key': 'health_amenity_type',
    'name': 'health_amenity_type',
    'description':
        'Indicates what types of speciality medical equipment '
        'is available at the healthsite',
    'options': [
        'ultrasound', 'mri', 'x_ray', 'dialysis', 'operating_theater',
        'laboratory', 'imaging_equipment', 'intensive_care_unit',
        'emergency_department'
    ],
    'required': False,
    'type': list,
}

dispensing = {
    'key': 'dispensing',
    'name': 'dispensing',
    'description':
        'Whether a pharmacy dispenses prescription drugs or not. '
        'Used to add information to something that is already '
        'tagged as amenity=pharmacy',
    'required': False,
    'type': bool,
}

wheelchair = {
    'key': 'wheelchair',
    'name': 'wheelchair',
    'description':
        'Used to mark places or ways that are suitable to be used '
        'with a wheelchair and a person with a disability who uses '
        'another mobility device (like a walker)',
    'required': False,
    'type': bool,
}

emergency = {
    'key': 'emergency',
    'name': 'emergency',
    'description': 'This key describes various emergency services',
    'required': False,
    'type': bool,
}

insurance = {
    'key': 'insurance',
    'name': 'insurance',
    'description':
        'This key describes the type of health '
        'insurance accepted at the healthsite',
    'options': [
        'no', 'public', 'private', 'unknown'
    ],
    'required': False,
    'type': list,
}

water_source = {
    'key': 'water_source',
    'name': 'water_source',
    'description':
        'Used to indicate the source of the water for '
        'features that provide or use water',
    'options': [
        'well', 'water_works', 'manual_pump', 'powered_pump',
        'groundwater', 'rain'
    ],
    'required': False,
    'type': str,
}

electricity = {
    'key': 'electricity',
    'name': 'electricity',
    'description': 'Used to indicate the source of the power generated',
    'options': [
        'grid', 'generator', 'solar', 'other', 'none'
    ],
    'required': False,
    'type': str,
}

is_in_health_area = {
    'key': 'is_in_health_area',
    'name': 'is_in_health_area',
    'description':
        'Used to capture the health area a health facility falls within',
    'required': False,
    'type': str,
}

is_in_health_zone = {
    'key': 'is_in_health_zone',
    'name': 'is_in_health_zone',
    'description':
        'Used to capture the health zone a health facility falls within',
    'required': False,
    'type': str,
}

url = {
    'key': 'url',
    'name': 'url',
    'description':
        'Specifying a url related to a feature, '
        'in this case the url if available',
    'required': False,
    'type': str,
}

ALL_TAGS = [
    amenity,
    healthcare,
    name,
    operator,
    source,
    speciality,
    operator_type,
    addr_full,
    contact_number,
    operational_status,
    opening_hours,
    beds,
    staff_doctors,
    staff_nurses,
    health_amenity_type,
    dispensing,
    wheelchair,
    emergency,
    insurance,
    water_source,
    electricity,
    is_in_health_area,
    is_in_health_zone,
    url,
]

MANDATORY_TAGS = [tag for tag in ALL_TAGS if tag.get('required')]


def get_mandatory_tags(osm_tags):
    """Get special mandatory tags based on requested osm data.

    :param osm_tags: OSM tags.
    :type osm_tags: dict

    :return: List of mandatory tags.
    :rtype: list
    """
    # Dispensing become mandatory if amenity is pharmacy
    if osm_tags.get('amenity') == 'pharmacy':
        return MANDATORY_TAGS + [dispensing]

    return MANDATORY_TAGS


# Healthcare speciality options
# https://wiki.openstreetmap.org/wiki/Key:healthcare#Subtags

speciality_options = {
    'clinic': [
        'abortion', 'fertility'
    ],
    'psychotherapist': [
        'behavior', 'body', 'depth', 'humanistic', 'other', 'systemic'
    ],
    'laboratory': [
        'biology', 'blood_check', 'clinical_pathology',
        'diagnostic_radiology', 'medical _physics', 'medical_engineering',
        'radiology'
    ],
    'alternative': [
        'acupuncture', 'anthroposophical', 'applied_kinesiology',
        'aromatherapy', 'ayurveda', 'chiropractic', 'herbalism', 'homeopathy',
        'hydrotherapy', 'hypnosis', 'naturopathy', 'osteopathy', 'reflexology',
        'reiki', 'shiatsu', 'traditional_chinese_medicine', 'tuina', 'unani'
    ],
}


def update_tag_options(tag_definition, osm_tags):
    """Update tag options in case of custom rule. e.g: speciality

    :param tag_definition: Definition of a tag.
    :type tag_definition: dict

    :param osm_tags: OSM tags.
    :type osm_tags: dict

    :return: Updated definition.
    :rtype: dict
    """
    tags_with_special_case = [
        {
            'tag': speciality['key'],
            'reference': healthcare['key'],
            'options': speciality_options,
        },
    ]
    for special_tag in tags_with_special_case:
        if not tag_definition['key'] == special_tag['tag']:
            continue
        reference_data = osm_tags.get(special_tag['reference'])
        if not isinstance(reference_data, list):
            reference_data = [reference_data]

        for value in reference_data:
            if value and special_tag['options'].get(value):
                tag_definition['options'].extend(special_tag['options'][value])

    return tag_definition
