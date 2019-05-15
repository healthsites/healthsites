# -*- coding: utf-8 -*-

# Healthsites related tags

amenity = {
    'key': 'amenity',
    'name': 'amenity',
    'description': '',
    'options': [
        'clinic', 'doctors', 'hospital', 'dentist', 'pharmacy'
    ],
    'required': True,
    'type': str,
}

healthcare = {
    'key': 'healthcare',
    'name': 'healthcare',
    'description': '',
    'options': [
        'doctor', 'pharmacy', 'hospital', 'clinic', 'dentist',
        'physiotherapist', 'alternative', 'laboratory', 'optometrist',
        'rehabilitation', 'blood_donation', 'birthing_center'
    ],
    'required': True,
    'type': str,
}

speciality = {
    'key': 'speciality',
    'name': 'speciality',
    'description': '',
    'options': [],
    'required': False,
    'type': str,
}

operator_type = {
    'key': 'operator_type',
    'name': 'operator_type',
    'description': '',
    'options': [
        'public', 'private', 'community', 'religious', 'government', 'ngo',
        'combination'
    ],
    'required': False,
    'type': str,
}

operational_status = {
    'key': 'operational_status',
    'name': 'operational_status',
    'description': '',
    'options': [
        'operational', 'non_operational', 'unknown'
    ],
    'required': False,
    'type': str,
}

health_amenity_type = {
    'key': 'health_amenity_type',
    'name': 'health_amenity_type',
    'description': '',
    'options': [
        'ultrasound', 'mri', 'x_ray', 'dialysis', 'operating_theater',
        'laboratory', 'imaging_equipment', 'intensive_care_unit',
        'emergency_department'
    ],
    'required': False,
    'type': str,
}

insurance_health = {
    'key': 'insurance_health',
    'name': 'insurance_health',
    'description': '',
    'options': [
        'no', 'public', 'private', 'unknown'
    ],
    'required': False,
    'type': str,
}

water_source = {
    'key': 'water_source',
    'name': 'water_source',
    'description': '',
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
    'description': '',
    'options': [
        'grid', 'generator', 'solar', 'other', 'none'
    ],
    'required': False,
    'type': str,
}

dispensing = {
    'key': 'dispensing',
    'name': 'dispensing',
    'description': '',
    'required': False,
    'type': bool,
}

wheelchair = {
    'key': 'wheelchair',
    'name': 'wheelchair',
    'description': '',
    'required': False,
    'type': bool,
}

emergency = {
    'key': 'emergency',
    'name': 'emergency',
    'description': '',
    'required': False,
    'type': bool,
}

ALL_TAGS = [
    amenity,
    healthcare,
    operator_type,
    operational_status,
    health_amenity_type,
    insurance_health,
    water_source,
    electricity,
    dispensing,
    wheelchair,
    emergency
]

MANDATORY_TAGS = [tag for tag in ALL_TAGS if tag.get('required')]


def get_mandatory_tags(osm_data):
    """Get special mandatory tags based on requested osm data.

    :param osm_data: OSM data.
    :type osm_data: dict

    :return: List of mandatory tags.
    :rtype: list
    """
    # Dispensing become mandatory if amenity is pharmacy
    if osm_data.get('amenity') == 'pharmacy':
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


def update_tag_options(tag_definition, osm_data):
    """Update tag options in case of custom rule. e.g: speciality

    :param tag_definition: Definition of a tag.
    :type tag_definition: dict

    :param osm_data: OSM data.
    :type osm_data: dict

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
        reference_data = osm_data.get(special_tag['reference'])
        if reference_data and special_tag['options'].get(reference_data):
            tag_definition['options'] = special_tag['options'][reference_data]

    return tag_definition
