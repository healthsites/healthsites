# -*- coding: utf-8 -*-
from unittest import skip

from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from mock import patch, MagicMock

from .model_factories import UserF, UserSocialAuthF


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_singin_view(self):
        resp = self.client.get(reverse('usersignpage'))

        self.assertEqual(resp.status_code, 200)

    @skip('skip')
    def test_profile_view(self):
        user = UserF(username='test1', password='test1')
        UserSocialAuthF.create(
            provider='openstreetmap',
            uid='2418849',
            extra_data='{"access_token":"qwertqwert"}',
            user=user
        )

        self.client.login(username='test1', password='test1')
        resp = self.client.get(reverse('userprofilepage'))

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.context['auths'], [u'openstreetmap'])
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'social_users/profilepage.html', u'base.html',
                u'pipeline/css.html', u'pipeline/js.html', u'pipeline/js.html'
            ]
        )

    @skip('skip')
    def test_profile_view_no_user(self):
        resp = self.client.get(reverse('userprofilepage'))
        self.assertRedirects(
            resp, '/signin/?next=/profile/',
            status_code=302, target_status_code=200
        )

    @patch('localities_osm.models.locality.LocalityOSMView')
    def test_logout_view(self, mock_locality_osm):  # noqa
        mock_locality_osm = MagicMock()  # noqa
        UserF(username='test1', password='test1')
        self.client.login(username='test1', password='test1')
        resp = self.client.get(reverse('logout_user'))

        self.assertRedirects(
            resp, '/', status_code=302, target_status_code=200
        )
