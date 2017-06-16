# -*- coding: utf-8 -*-

import mock

from django.contrib.auth.models import User
from django.test import TestCase

from social_users.tests.model_factories import ProfileF, UserF

from ..middleware import profile_picture_url, save_profile


class TestMiddleware(TestCase):
    def test_response_with_profile(self):
        user = UserF(username='test1', password='test1')
        profile = ProfileF(user=user)

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = 'picture?type=large'

            MockBackend = mock.Mock()

            user_obj = save_profile(MockBackend, user, {}, is_new=False)

        profile.refresh_from_db()

        self.assertEqual(
            profile.profile_picture, 'picture?type=large'
        )

        self.assertEqual(user.profile.id, profile.id)

        self.assertTrue('user' in user_obj)

        self.assertTrue(user_obj['user'].id == user.id)

    def test_response_no_profile(self):
        user = UserF(username='test1', password='test1')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = 'picture?type=large'

            MockBackend = mock.Mock()

            save_profile(MockBackend, user, {}, is_new=False)

        self.assertEqual(
            user.profile.profile_picture, 'picture?type=large'
        )

    def test_no_backend_no_profile(self):
        user = UserF(username='test1', password='test1')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = None

            MockBackend = mock.Mock()

            save_profile(MockBackend, user, {}, is_new=False)

        self.assertEqual(
            user.profile.profile_picture, ''
        )

    def test_new_user_replaces_old(self):
        user = UserF(username='test1', password='test1')
        UserF(username='test2', password='test2')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = None

            MockBackend = mock.Mock()

            kwargs = {'details': {'username': 'test 2'}}
            save_profile(MockBackend, user, {}, is_new=True, **kwargs)

        users = User.objects.all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'test2')

    def test_new_user_old_does_not_exist(self):
        user = UserF(username='test1', password='test1')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = None

            MockBackend = mock.Mock()

            kwargs = {'details': {'username': 'test 2'}}
            save_profile(MockBackend, user, {}, is_new=True, **kwargs)

        users = User.objects.all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'test1')

    def test_new_user_no_username_data(self):
        user = UserF(username='test1', password='test1')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = None

            MockBackend = mock.Mock()

            kwargs = {'details': {}}
            save_profile(MockBackend, user, {}, is_new=True, **kwargs)

        users = User.objects.all()

        self.assertEqual(users[0].username, 'test1')

    def test_new_user_same_username(self):
        user = UserF(username='test1', password='test1')

        with mock.patch('social_users.middleware.profile_picture_url') as mock_ppurl:
            mock_ppurl.return_value = None

            MockBackend = mock.Mock()

            kwargs = {'details': {'username': 'test 1'}}
            save_profile(MockBackend, user, {}, is_new=True, **kwargs)

        users = User.objects.all()

        self.assertEqual(users[0].username, 'test1')


class TestProfilePictureUrl(TestCase):
    def test_profile_picture_url_unknown_backend(self):
        MockBackend = mock.Mock()

        response = {}

        result = profile_picture_url(backend=MockBackend, response=response)

        self.assertIsNone(result)

    def test_profile_picture_url_facebook_backend(self):
        MockBackend = mock.Mock()
        MockBackend.name = 'facebook'

        response = {
            'id': 12
        }

        result = profile_picture_url(backend=MockBackend, response=response)

        self.assertEqual(result, 'http://graph.facebook.com/12/picture?type=large')

    def test_profile_picture_url_twitter_backend(self):
        MockBackend = mock.Mock()
        MockBackend.name = 'twitter'

        response = {
            'profile_image_url': 'profile_images/_normal_jRVAra5A.jpeg'
        }

        result = profile_picture_url(backend=MockBackend, response=response)

        self.assertEqual(result, 'profile_images/_jRVAra5A.jpeg')

    def test_profile_picture_url_googleoauth2_backend(self):
        MockBackend = mock.Mock()
        MockBackend.name = 'google-oauth2'

        response = {
            'image': {
                'url': 'test_url'
            }
        }

        result = profile_picture_url(backend=MockBackend, response=response)

        self.assertEqual(result, 'test_url')
