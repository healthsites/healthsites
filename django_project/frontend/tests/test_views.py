# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'main.html', u'base.html', u'pipeline/css.html',
                u'pipeline/js.html', u'pipeline/js.html'
            ]
        )
