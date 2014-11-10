# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.conf import settings


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['debug'], False)

        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'main.html', u'base.html', u'pipeline/css.html',
                u'pipeline/js.html', u'pipeline/js.html'
            ]
        )

    def test_home_view_no_googleanalytics(self):
        # specifically set DEBUG to True
        settings.DEBUG = True

        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['debug'], True)
        self.assertTrue(resp.content.find('GoogleAnalyticsObject') == -1)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'main.html', u'base.html', u'pipeline/css.html',
                u'pipeline/js.html', u'pipeline/js.html'
            ]
        )

    def test_about_view(self):
        resp = self.client.get(reverse('about'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'about.html'
            ]
        )

    def test_help_view(self):
        resp = self.client.get(reverse('help'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'help.html'
            ]
        )
