# -*- coding: utf-8 -*-
from django.test import TestCase

from ..utils import render_fragment


class TestUtils(TestCase):
    def test_render_fragment(self):
        template = 'test {{ obj.data }}'
        context = {'obj': {'data': 'test'}}

        self.assertEqual(render_fragment(template, context), u'test test')
