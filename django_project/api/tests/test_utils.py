# -*- coding: utf-8 -*-

from django.test import TestCase

from ..utils import remap_dict


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
