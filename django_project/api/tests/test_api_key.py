# coding=utf-8

from django.test import TestCase, Client
from django.urls import reverse

from api.models.user_api_key import UserApiKey
from core.models.preferences import SitePreferences
from core.tests.model_factories.user import UserF


class TestApiKey(TestCase):

    def setUp(self):
        """To setup tests."""
        preference = SitePreferences.preferences()
        preference.site_url = 'http://test.com'
        preference.save()
        self.preference = preference

        self.username = 'test'
        self.password = 'test'
        self.user = UserF(
            username=self.username,
            password=self.password
        )
        self.api_key = UserApiKey.objects.create(
            user=self.user,
            api_key=UserApiKey.generate_key()
        )

    def test_api_v1_v2(self):
        """Test enrollment."""
        client = Client()
        client.login(username=self.user.username, password=self.password)
        url = reverse('user-detail') + '?api-key=test'
        url = url.replace('v3', 'v1')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deprecated' in str(response.content))
        url = url.replace('v3', 'v2')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deprecated' in str(response.content))

    def test_api_v3_without_correct_api_key(self):
        """Test enrollment."""
        client = Client()
        url = reverse('user-detail') + '?api-key=test'
        response = client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.preference.site_url in str(response.content))

    def test_api_v3_with_correct_api_key_but_not_active(self):
        """Test enrollment."""
        client = Client()
        url = reverse('user-detail') + f'?api-key={self.api_key}'
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_api_v3_with_correct_api_key(self):
        """Test enrollment."""
        client = Client()
        self.api_key.is_active = True
        self.api_key.save()
        url = reverse('user-detail') + f'?api-key={self.api_key}'
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_v3_with_correct_api_key_with_limit(self):
        """Test enrollment."""
        client = Client()
        self.preference.default_max_request_api = 1
        self.preference.save()
        self.api_key.is_active = True
        self.api_key.save()

        url = reverse('user-detail') + f'?api-key={self.api_key}'
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('user-detail') + f'?api-key={self.api_key}'
        response = client.get(url)
        self.assertEqual(response.status_code, 403)
