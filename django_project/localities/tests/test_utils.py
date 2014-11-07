# -*- coding: utf-8 -*-
from django.test import TestCase

from ..utils import render_fragment, detect_data_changes, ramify_data


class TestUtils(TestCase):
    def test_render_fragment(self):
        template = 'test {{ obj.data }}'
        context = {'obj': {'data': 'test'}}

        self.assertEqual(render_fragment(template, context), u'test test')

    def test_detect_data_changes(self):
        original_data = {
            'lat': 0,
            'lon': 0,
            'test': 'initial_data',
            'should_not_be_visible': True
        }
        new_data = {
            'lat': 0,
            'lon': 0,
            'test': 'changed_data',
            'new_data': 'new_data'
        }

        self.assertEqual(
            detect_data_changes(original_data, new_data),
            ['test', 'new_data']
        )

    def test_ramify_data(self):
        initial_data = {
            'lat': 0,
            'lon': 0,
            'test': 'initial_data',
            'should_not_be_visible': True
        }
        candidate_keys = {'lat', 'lon'}

        first, second = ramify_data(initial_data, candidate_keys)
        self.assertListEqual(first.keys(), ['lat', 'lon'])
        self.assertListEqual(second.keys(), ['test', 'should_not_be_visible'])

    def test_ramify_data_bad_keys(self):
        initial_data = {
            'lat': 0,
            'lon': 0,
            'test': 'initial_data',
            'should_not_be_visible': True
        }
        candidate_keys = {'X_lat', 'lon', 'bad_key'}

        first, second = ramify_data(initial_data, candidate_keys)
        self.assertListEqual(first.keys(), ['lon'])
        self.assertListEqual(
            second.keys(), ['lat', 'test', 'should_not_be_visible']
        )
