# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from mock import patch, MagicMock


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('localities_osm.models.locality.LocalityOSMView')
    def test_home_view(self, mock_locality_osm):
        mock_locality_osm = MagicMock()
        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['debug'], False)

    @patch('localities_osm.models.locality.LocalityOSMView')
    def test_home_view_no_googleanalytics(self, mock_locality_osm):
        mock_locality_osm = MagicMock()
        # specifically set DEBUG to True
        settings.DEBUG = True

        resp = self.client.get(reverse('home'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['debug'], True)
        self.assertTrue(resp.content.find('GoogleAnalyticsObject') == -1)

    @patch('localities_osm.models.locality.LocalityOSMView')
    def test_about_view(self, mock_locality_osm):
        mock_locality_osm = MagicMock()
        resp = self.client.get(reverse('about'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'about.html'
            ]
        )

    @patch('localities_osm.models.locality.LocalityOSMView')
    def test_help_view(self, mock_locality_osm):
        mock_locality_osm = MagicMock()
        resp = self.client.get(reverse('help'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'help.html'
            ]
        )
