# -*- coding: utf-8 -*-
from django.test import TestCase

from ..utils import render_fragment, parse_bbox


class TestUtils(TestCase):
    def test_render_fragment(self):
        template = 'test {{ obj.data }}'
        context = {'obj': {'data': 'test'}}

        self.assertEqual(render_fragment(template, context), u'test test')

    def test_parse_bbox(self):
        self.assertRaises(ValueError, parse_bbox, '-180,90,-a,-b')

    def test_parse_bbox_bad(self):
        self.assertRaises(ValueError, parse_bbox, '-180,90,180,-90')

        self.assertRaises(ValueError, parse_bbox, '180,-90,-180,90')

    def test_parse_bbox_return(self):
        self.assertEqual(
            parse_bbox('-180,-90,180,90').wkt,
            u'POLYGON ((-180.0000000000000000 -90.0000000000000000, -180.00000'
            u'00000000000 90.0000000000000000, 180.0000000000000000 90.0000000'
            u'000000000, 180.0000000000000000 -90.0000000000000000, -180.00000'
            u'00000000000 -90.0000000000000000))'
        )
