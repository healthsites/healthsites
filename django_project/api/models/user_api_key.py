__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

import binascii
import os

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.validators import URLValidator
from django.utils import timezone

from core.models.preferences import SitePreferences


class UserApiKey(models.Model):
    """
    This model provide user API KEY to access API of healthsites
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    api_key = models.CharField(
        max_length=40, primary_key=True
    )
    is_active = models.BooleanField(
        default=False
    )
    allow_write = models.BooleanField(
        default=False,
        help_text='Allow this api key to write data'
    )
    max_request_per_day = models.IntegerField(
        help_text=(
            'Max request per day for the api key. '
            'If it is empty, it will use default_max_request_api preference.'
        ),
        null=True, blank=True
    )

    @property
    def limit(self):
        """Return limit of request."""
        if self.max_request_per_day is None:
            preference = SitePreferences.load()
            return preference.default_max_request_api
        return self.max_request_per_day

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.api_key

    @staticmethod
    def get_user_from_api_key(api_key):
        """ return user from API Key

        :param api_key: user that going to be checked
        :type api_key: User

        :return: User found or None
        :rtype: User
        """
        try:
            return UserApiKey.objects.get(
                api_key=api_key,
                is_active=True
            ).user
        except UserApiKey.DoesNotExist:
            return None

    @staticmethod
    def get_key_from_api_key(api_key):
        """ return user from API Key

        :param api_key: user that going to be checked
        :type api_key: User

        :return: UserApiKey
        :rtype: UserApiKey
        """
        try:
            return UserApiKey.objects.get(
                api_key=api_key
            )
        except UserApiKey.DoesNotExist:
            return None


class ApiKeyAccess(models.Model):
    """API Key Access."""

    api_key = models.ForeignKey(UserApiKey, on_delete=models.CASCADE)
    date = models.DateField()
    counter = models.IntegerField(default=0)

    @staticmethod
    def request(api_key: UserApiKey, url: str, method: str):
        """Doing a request."""
        now = timezone.now()
        date = now.date()
        access, _ = ApiKeyAccess.objects.get_or_create(
            api_key=api_key, date=date
        )
        access.counter += 1
        if access.counter > api_key.limit:
            return False

        access.save()
        ApiKeyRequestLog.objects.create(
            api_key=api_key, time=now, url=url, method=method
        )
        return True


class ApiKeyRequestLog(models.Model):
    """API Key for request log."""

    api_key = models.ForeignKey(UserApiKey, on_delete=models.CASCADE)
    method = models.CharField(max_length=126)
    time = models.DateTimeField()
    url = models.TextField()


class ApiKeyEnrollment(models.Model):
    """API Key enrollment data."""

    contact_person = models.CharField(max_length=512)
    contact_email = models.EmailField()
    organisation_name = models.CharField(max_length=512)
    organisation_url = models.CharField(
        max_length=512, validators=[URLValidator()]
    )
    project_url = models.CharField(
        max_length=512,
        help_text='web site or project URL for API will be used',
        validators=[URLValidator()]
    )
    time = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=False,
        help_text='When approved, the api_key will be created and activated'
    )
    api_key = models.OneToOneField(
        UserApiKey, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        super(ApiKeyEnrollment, self).save(*args, **kwargs)
        if self.api_key:
            self.api_key.is_active = self.approved
            self.api_key.save()

    def generate_api_key(self, user: User):
        """Generating api key."""
        if not self.api_key:
            api_key = UserApiKey(
                user=user, is_active=False
            )
            api_key.api_key = UserApiKey.generate_key()
            api_key.save()
            self.api_key = api_key
            self.save()
