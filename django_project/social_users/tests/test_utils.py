# -*- coding: utf-8 -*-

from django.test import Client, TestCase

from ..utils import clean_website, get_profile
from .model_factories import (
    OrganisationF, ProfileF, UserF, UserSocialAuthF, UserWith2OrganisationSupportedF
)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_userprofile_does_not_exist(self):
        user = UserF(username='test1', password='test1')

        profile = get_profile(user)

        self.assertEqual(profile.profile_picture, '')

    def test_userprofile_does_exist(self):
        user = UserF(username='test1', password='test1')
        ProfileF(user=user, profile_picture='this is a picture')

        profile = get_profile(user)

        self.assertEqual(profile.profile_picture, 'this is a picture')

    def test_user_social_provider_facebook(self):
        user = UserF(username='test1', password='test1')

        UserSocialAuthF.create(
            provider='facebook',
            uid='123',
            user=user
        )

        profile = get_profile(user)

        self.assertEqual(len(profile.social), 1)
        self.assertDictEqual(profile.social[0], {'provider': 'facebook', 'uid': '123'})

    def test_user_social_provider_twitter(self):
        user = UserF(username='test1', password='test1')

        UserSocialAuthF.create(
            provider='twitter',
            uid='123',
            user=user
        )

        profile = get_profile(user)

        self.assertEqual(len(profile.social), 1)
        self.assertDictEqual(profile.social[0], {'provider': 'twitter', 'uid': user.username})

    def test_user_with_2_organisationsupported(self):
        user = UserF()

        org1 = OrganisationF(name='Global Org')
        org2 = OrganisationF(name='Local Org')

        UserWith2OrganisationSupportedF(
            user=user,
            orgsupported1__organisation=org1,
            orgsupported1__is_staff=True,
            orgsupported2__organisation=org2
        )

        profile = get_profile(user)

        self.assertTrue(profile.is_trusted_user)

        self.assertEqual(len(profile.organisations), 1)
        self.assertDictEqual(
            profile.organisations[0], {'name': org1.name, 'website': 'http://healthsites.io'}
        )

        self.assertEqual(len(profile.organisations_supported), 1)
        self.assertDictEqual(
            profile.organisations_supported[0],
            {'name': org2.name, 'website': 'http://healthsites.io'}
        )

    def test_clean_website_contains_http(self):
        site_domain = 'http://healthsites.io'

        self.assertEqual(clean_website(site_domain), 'http://healthsites.io')

    def test_clean_website_without_http(self):
        site_domain = 'healthsites.io'

        self.assertEqual(clean_website(site_domain), 'http://healthsites.io')
