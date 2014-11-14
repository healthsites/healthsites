# -*- coding: utf-8 -*-
from django.test import TestCase


from ..models import LocalityIndex


class TestModelLocalityIndex(TestCase):
    def test_LocalityIndex_fields(self):
        self.assertListEqual(
            [fld.name for fld in LocalityIndex._meta.fields], [
                u'id', 'locality', 'ranka', 'rankb', 'rankc', 'rankd',
                'fts_index'
            ]
        )
