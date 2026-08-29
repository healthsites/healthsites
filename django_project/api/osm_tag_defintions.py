# -*- coding: utf-8 -*-


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

# Healthsites related tags
# Mandatory tags - see https://github.com/healthsites/healthsites/issues/1129

amenity = {
    'key': 'amenity',
    'name': 'amenity',
    'description': (
        'The primary OSM tag for health facilities. '
        'Describes the type of amenity provided.'
    ),
    'options': [
        'clinic', 'doctors', 'hospital', 'dentist', 'pharmacy'
    ],
    'required': True,
    'type': str,
}

healthcare = {
    'key': 'healthcare',
    'name': 'healthcare',
    'description': (
        'Classifies the facility within the healthcare sector. '
        'Use alongside amenity to provide full context.'
    ),
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
    'description': 'The official name of the health facility.',
    'required': True,
    'type': str,
}

operator = {
    'key': 'operator',
    'name': 'operator',
    'description': (
        'The name of the organisation, company, or individual '
        'directly responsible for operating the facility.'
    ),
    'required': False,
    'type': str,
}

# TODO : we hide this for now
# source = {
#     'key': 'source',
#     'name': 'source',
#     'description':
#         'Used to indicate the source of information '
#         '(i.e. meta data) added to OpenStreetMap',
#     'required': False,
#     'type': str,
# }

# Not mandatory tags
speciality = {
    'key': 'speciality',
    'name': 'speciality',
    'description': (
        'The medical speciality or specialities offered by the facility. '
        'Use in conjunction with healthcare=*. '
        'For example: healthcare=laboratory and speciality=blood_check.'
    ),
    'options': [
        'allergology',
        'anatomy',
        'anaesthetics',
        'biochemistry',
        'biological_haematology',
        'biology',
        'cardiology',
        'cardiac_surgery',
        'child_psychiatry',
        'community',
        'dental_oral_maxillo_facial_surgery',
        'dermatology',
        'dermatovenereology',
        'diagnostic_radiology',
        'emergency',
        'endocrinology',
        'gastroenterological_surgery',
        'gastroenterology',
        'general',
        'geriatrics',
        'gynaecology',
        'haematology',
        'hepatology',
        'immunology',
        'infectious_diseases',
        'intensive',
        'internal',
        'maxillofacial_surgery',
        'microbiology',
        'nephrology',
        'neurology',
        'neurophysiology',
        'neuropsychiatry',
        'neurosurgery',
        'nuclear',
        'occupational',
        'oncology',
        'ophthalmology',
        'orthodontics',
        'orthopaedics',
        'otolaryngology',
        'paediatric_surgery',
        'paediatrics',
        'palliative',
        'pathology',
        'pharmacology',
        'physiatry',
        'plastic_surgery',
        'podiatry',
        'proctology',
        'psychiatry',
        'pulmonology',
        'radiology',
        'radiotherapy',
        'rheumatology',
        'stomatology',
        'surgery',
        'surgical_oncology',
        'thoracic_surgery',
        'transplant',
        'trauma',
        'tropical',
        'urology',
        'vascular_surgery',
        'vaccination',
        'venereology'
    ],
    'options_dependent': {
        'depend_on': 'healthcare',
        'options': speciality_options
    },
    'required': False,
    'type': list,
}

operator_type = {
    'key': 'operator_type',
    'name': 'operator_type',
    'description': (
        'The ownership or management type of the facility operator.'
    ),
    'options': [
        'public', 'private', 'community', 'religious', 'government', 'ngo',
        'combination'
    ],
    'required': False,
    'type': str,
}

contact_number = {
    'key': 'contact_number',
    'name': 'contact_number',
    'description': 'Phone number for contacting the facility.',
    'required': False,
    'type': str,
}

operational_status = {
    'key': 'operational_status',
    'name': 'operational_status',
    'description': 'The current operational status of the facility.',
    'options': [
        'operational', 'non_operational', 'unknown'
    ],
    'required': False,
    'type': str,
}

opening_hours = {
    'key': 'opening_hours',
    'name': 'opening_hours',
    'description': (
        'The opening hours of the facility in OSM format. '
        'Example: Mo-Fr 08:00-17:00.'
    ),
    'required': False,
    'type': str,
}

beds = {
    'key': 'beds',
    'name': 'beds',
    'description': 'The total number of beds available at the facility.',
    'required': False,
    'type': int,
}

staff_doctors = {
    'key': 'staff_doctors',
    'name': 'staff_doctors',
    'description': 'The number of doctors employed at the facility.',
    'required': False,
    'type': int,
}

staff_nurses = {
    'key': 'staff_nurses',
    'name': 'staff_nurses',
    'description': 'The number of nurses employed at the facility.',
    'required': False,
    'type': int,
}

health_amenity_type = {
    'key': 'health_amenity_type',
    'name': 'health_amenity_type',
    'description': (
        'Speciality medical equipment or services available at the facility.'
    ),
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
    'description': (
        'Whether the pharmacy dispenses prescription drugs. '
        'Applies to facilities tagged as amenity=pharmacy.'
    ),
    'required': False,
    'type': bool,
}

wheelchair = {
    'key': 'wheelchair',
    'name': 'wheelchair',
    'description': 'Whether the facility is accessible by wheelchair.',
    'required': False,
    'type': bool,
}

emergency = {
    'key': 'emergency',
    'name': 'emergency',
    'description': 'Whether the facility provides emergency services.',
    'required': False,
    'type': bool,
}

insurance = {
    'key': 'insurance',
    'name': 'insurance',
    'description': 'The type of health insurance accepted at the facility.',
    'options': [
        'no', 'public', 'private', 'unknown'
    ],
    'required': False,
    'type': list,
}

water_source = {
    'key': 'water_source',
    'name': 'water_source',
    'description': 'The source of water supply for the facility.',
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
    'description': 'The source of electricity supply for the facility.',
    'options': [
        'grid', 'generator', 'solar', 'other', 'none'
    ],
    'required': False,
    'type': str,
}

is_in_health_area = {
    'key': 'is_in_health_area',
    'name': 'is_in_health_area',
    'description': 'The health area (administrative division) the facility belongs to.',
    'required': False,
    'type': str,
}

is_in_health_zone = {
    'key': 'is_in_health_zone',
    'name': 'is_in_health_zone',
    'description': 'The health zone (administrative division) the facility belongs to.',
    'required': False,
    'type': str,
}

url = {
    'key': 'url',
    'name': 'url',
    'description': 'The website URL of the facility.',
    'required': False,
    'type': str,
}

# ADDRESS
addr_housenumber = {
    'key': 'addr_housenumber',
    'name': 'addr_housenumber',
    'description': 'The house or building number of the facility address.',
    'required': False,
    'type': str,
}
addr_street = {
    'key': 'addr_street',
    'name': 'addr_street',
    'description': 'The street name of the facility address.',
    'required': False,
    'type': str,
}
addr_postcode = {
    'key': 'addr_postcode',
    'name': 'addr_postcode',
    'description': 'The postcode of the facility address.',
    'required': False,
    'type': str,
}
addr_city = {
    'key': 'addr_city',
    'name': 'addr_city',
    'description': 'The city of the facility address.',
    'required': False,
    'type': str,
}

ALL_TAGS = [
    amenity,
    healthcare,
    name,
    operator,
    # source, # TODO: hide it for now
    speciality,
    operator_type,
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

    addr_housenumber,
    addr_street,
    addr_postcode,
    addr_city
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