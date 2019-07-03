# -*- coding: utf-8 -*-

import os

from django.test import TestCase

from api.osm_field_definitions import ALL_FIELDS
from api.utils import validate_osm_tags, get_osm_schema
from ..utils import remap_dict, convert_to_osm_tag


class TestUtils(TestCase):

    def test_remap_dict(self):
        old_dict = {'a': 1, 'b': 1}
        new_dict = remap_dict(old_dict, {})

        self.assertEqual(new_dict, {'a': 1, 'b': 1})

        old_dict = {'a': 1, 'b': 1}
        new_dict = remap_dict(old_dict, {'b': 'new_b'})

        self.assertEqual(new_dict, {'a': 1, 'new_b': 1})

        old_dict = {'a': 1, 'b': 1}
        new_dict = remap_dict(old_dict, {'a': 'new_a', 'b': 'new_b'})

        self.assertEqual(new_dict, {'new_a': 1, 'new_b': 1})

    def test_convert_osm_tags(self):
        old_dict = {
            'speciality': 'healthsites specialty',
            'addr_full': 'healthsites street',
            'contact_number': 'healthsites phone number'
        }
        expected_dict = {
            'healthcare:speciality': 'healthsites specialty',
            'addr:full': 'healthsites street',
            'contact:phone': 'healthsites phone number'
        }

        mapping_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures', 'mapping.yml')

        self.assertEqual(
            convert_to_osm_tag(mapping_file_path, old_dict, 'node'),
            expected_dict)

        self.assertEqual(
            convert_to_osm_tag(mapping_file_path, old_dict, 'way'),
            expected_dict)

    def test_validate_osm_data(self):
        # test invalid mandatory tags
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'healthcare': 'clinic'
        }
        expected_message = 'Invalid OSM tags: `amenity` tag is missing.'
        status, actual_message = validate_osm_tags(tags)
        self.assertFalse(status)
        self.assertEqual(actual_message, expected_message)

        # test valid mandatory tags
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 'clinic',
            'healthcare': 'clinic'
        }
        status, _ = validate_osm_tags(tags)
        self.assertTrue(status)

        # test mandatory tags for amenity=pharmacy
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 'pharmacy',
            'healthcare': 'clinic'
        }
        status, actual_message = validate_osm_tags(tags)
        expected_message = 'Invalid OSM tags: `dispensing` tag is missing.'
        self.assertFalse(status)
        self.assertEqual(actual_message, expected_message)

        tags.update({'dispensing': True})
        status, _ = validate_osm_tags(tags)
        self.assertTrue(status)

        # test invalid value
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 'not a clinic',
            'healthcare': 'clinic'
        }
        status, actual_message = validate_osm_tags(tags)
        expected_message = (
            'Invalid value for key `amenity`: '
            'not a clinic is not a valid option.')
        self.assertFalse(status)
        self.assertEqual(actual_message, expected_message)

        # test invalid value type
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 0,
            'healthcare': 'clinic'
        }
        status, actual_message = validate_osm_tags(tags)
        expected_message = (
            'Invalid value for key `amenity`: 0 is not a valid option.')
        self.assertFalse(status)
        self.assertEqual(actual_message, expected_message)

        # test invalid speciality
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 'clinic',
            'healthcare': 'clinic',
            'speciality': 'radiology'
        }
        status, actual_message = validate_osm_tags(tags)
        expected_message = (
            'Invalid value for key `speciality`: '
            'radiology is not a valid option.')
        self.assertFalse(status)
        self.assertEqual(actual_message, expected_message)

        # test valid speciality
        tags = {
            'name': 'the name',
            'source': 'test case',
            'operator': 'the operator',
            'amenity': 'clinic',
            'healthcare': 'clinic',
            'speciality': 'abortion'
        }
        status, _ = validate_osm_tags(tags)
        self.assertTrue(status)

    def test_get_osm_schema(self):
        schema = get_osm_schema()
        self.assertListEqual(
            schema['facilities']['create']['fields'],
            ALL_FIELDS)
