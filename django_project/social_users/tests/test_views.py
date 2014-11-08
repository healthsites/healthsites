# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .model_factories import UserSocialAuthF


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_singin_view(self):
        resp = self.client.get(reverse('usersignpage'))

        self.assertEqual(resp.status_code, 200)

        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'social_users/signinpage.html', u'base.html',
                u'pipeline/css.html', u'pipeline/js.html', u'pipeline/js.html'
            ]
        )

    def test_profile_view(self):
        user = UserSocialAuthF.create(
            provider='openstreetmap',
            uid='2418849',
            extra_data='{"access_token":"qwertqwert"}'
        )
        user.user.set_password('test')
        user.user.save()
        self.client.login(username='username1', password='test')
        resp = self.client.get(reverse('userprofilepage'))
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(resp.context['auths'], [u'openstreetmap'])
        self.assertListEqual(
            [tmpl.name for tmpl in resp.templates], [
                'social_users/profilepage.html', u'base.html',
                u'pipeline/css.html', u'pipeline/js.html', u'pipeline/js.html'
            ]
        )
