# coding=utf-8

from django.test import TestCase, Client
from django.urls import reverse

from api.models.user_api_key import ApiKeyEnrollment
from core.models.preferences import SitePreferences
from core.tests.model_factories.user import UserF


class TestEnrollment(TestCase):

    def setUp(self):
        """To setup tests."""
        preference = SitePreferences.preferences()
        self.username = 'test'
        self.password = 'test'
        self.user = UserF(
            username=self.username,
            password=self.password
        )

    def test_enrollment_error(self):
        """Test enrollment."""
        client = Client()
        client.login(username=self.user.username, password=self.password)
        url = reverse('enrollment-form')
        response = client.post(url, data={
            'contact_person': 'Name Test',
            'contact_email': 'test@gmail.com',
            'organisation_name': 'Organisation Test',
            'organisation_url': 'organisation.com',
            'project_url': 'project.com',
        })
        self.assertEqual(response.status_code, 200)

    def test_enrollment_success(self):
        """Test enrollment."""
        client = Client()
        client.login(username=self.user.username, password=self.password)
        url = reverse('enrollment-form')
        response = client.post(url, data={
            'contact_person': 'Name Test',
            'contact_email': 'test@gmail.com',
            'organisation_name': 'Organisation Test',
            'organisation_url': 'http://organisation.com',
            'project_url': 'http://project.com',
        })
        self.assertEqual(response.status_code, 302)
        enrollment = ApiKeyEnrollment.objects.filter(
            api_key__user=self.user
        ).first()
        self.assertIsNotNone(enrollment)
        self.assertFalse(enrollment.approved)
        api_key = enrollment.api_key
        self.assertFalse(api_key.is_active)

        # Activate it
        enrollment.approved = True
        enrollment.save()
        self.assertTrue(enrollment.approved)
        self.assertTrue(api_key.is_active)
