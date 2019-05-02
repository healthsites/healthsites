# -*- coding: utf-8 -*-

import os

from django.test import TestCase

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
            'contact_number': 'healthsotes phone number'
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
