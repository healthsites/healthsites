# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '25/02/19'

from django.test import TestCase
from localities_osm.utilities import (
    convert_into_osm_dict,
    split_osm_and_extension_attr
)
from localities_osm.models.locality import LocalityOSM
from localities.tests.model_factories import (
    AttributeF,
    LocalityValue4F,
    LocalityValue1F
)
from social_users.tests.model_factories import UserF


class AttributeConverterUtilityTest(TestCase):

    def setUp(self):
        self.user = UserF.create(**{
            'username': 'anita',
            'is_staff': True
        })
        self.user.set_password('password')
        self.user.save()
        self.attr = AttributeF.create(key='facility')
        self.attr2 = AttributeF.create(key='staff')
        self.attr3 = AttributeF.create(key='inpatient_service')
        self.attr4 = AttributeF.create(key='scope_of_service')
        self.locality = LocalityValue4F.create(
            name='locality test',
            val1__data='building',
            val1__specification__attribute=self.attr,
            val2__data='15|18',
            val2__specification__attribute=self.attr2,
            val3__data='5|7',
            val3__specification__attribute=self.attr3,
            val4__data=
            'specialized care|general acute care|rehabilitation care|',
            val4__specification__attribute=self.attr4,
        )

    def test_convert_into_osm_dict(self):
        """Test converting old locality dict into osm dict."""

        osm_data_dict = convert_into_osm_dict(self.locality)
        self.assertEqual(osm_data_dict['name'], 'locality test')
        self.assertEqual(osm_data_dict['staff_nurses'], '18')
        self.assertEqual(osm_data_dict['staff_doctors'], '15')
        self.assertEqual(osm_data_dict['inpatient_service'], '12')
        self.assertEqual(
            osm_data_dict['scope_of_service'],
            ['specialized care', 'general acute care', 'rehabilitation care'])
        self.assertEqual(osm_data_dict['facility'], 'building')

        locality0 = LocalityValue1F.create(
            name='locality test',
            val1__data='5|',
            val1__specification__attribute=self.attr3,
        )
        osm_data_dict = convert_into_osm_dict(locality0)
        self.assertEqual(osm_data_dict['inpatient_service'], '5')

        locality1 = LocalityValue1F.create(
            name='locality test',
            val1__data='|3',
            val1__specification__attribute=self.attr3,
        )
        osm_data_dict = convert_into_osm_dict(locality1)
        self.assertEqual(osm_data_dict['inpatient_service'], '3')

        locality2 = LocalityValue1F.create(
            name='locality test',
            val1__data='',
            val1__specification__attribute=self.attr3,
        )
        osm_data_dict = convert_into_osm_dict(locality2)
        self.assertEqual(osm_data_dict['inpatient_service'], '0')

        locality3 = LocalityValue1F.create(
            name='locality test',
            val1__data='|',
            val1__specification__attribute=self.attr3,
        )
        osm_data_dict = convert_into_osm_dict(locality3)
        self.assertEqual(osm_data_dict['inpatient_service'], '0')

        locality4 = LocalityValue1F.create(
            name='locality test',
            val1__data='5|',
            val1__specification__attribute=self.attr2,
        )
        osm_data_dict = convert_into_osm_dict(locality4)
        self.assertEqual(osm_data_dict['staff_doctors'], '5')
        self.assertEqual(osm_data_dict['staff_nurses'], '0')

        locality5 = LocalityValue1F.create(
            name='locality test',
            val1__data='|2',
            val1__specification__attribute=self.attr2,
        )
        osm_data_dict = convert_into_osm_dict(locality5)
        self.assertEqual(osm_data_dict['staff_doctors'], '0')
        self.assertEqual(osm_data_dict['staff_nurses'], '2')

        locality6 = LocalityValue1F.create(
            name='locality test',
            val1__data='|',
            val1__specification__attribute=self.attr2,
        )
        osm_data_dict = convert_into_osm_dict(locality6)
        self.assertEqual(osm_data_dict['staff_doctors'], '0')
        self.assertEqual(osm_data_dict['staff_nurses'], '0')

    def test_split_osm_attr_and_extension(self):
        """Test splitting osm attributes and extension attributes."""

        osm_data_dict = convert_into_osm_dict(self.locality)
        osm_attr, extension_attr = \
            split_osm_and_extension_attr(osm_data_dict)

        self.assertEqual(extension_attr['facility'], 'building')
        self.assertEqual(
            extension_attr['scope_of_service'],
            ['specialized care', 'general acute care', 'rehabilitation care'])
        self.assertEqual(
            extension_attr.keys(), ['facility', 'scope_of_service'])
        self.assertItemsEqual(
            osm_attr.keys(),
            ['speciality', 'osm_id', 'operator', 'operation', 'water_source',
             'changeset_id', 'insurance', 'staff_doctors', 'category',
             'contact_number', 'raw_data_archive_url', 'source', 'type',
             'status', 'wheelchair_access', 'physical_address', 'emergency',
             'changeset_timestamp', 'nature_of_facility', 'ownership', 'name',
             'staff_nurses', 'changeset_user', 'changeset_version',
             'dispensing', 'power_source', 'inpatient_service']
        )

        osm_fields = LocalityOSM._meta.get_all_field_names()
        self.assertItemsEqual(
            osm_attr.keys(),
            osm_fields
        )

        self.assertEqual(osm_attr['inpatient_service'], '12')
        self.assertEqual(osm_attr['physical_address'], '')
        self.assertEqual(osm_attr['name'], 'locality test')
        self.assertEqual(osm_attr['staff_nurses'], '18')
        self.assertEqual(osm_attr['staff_doctors'], '15')
