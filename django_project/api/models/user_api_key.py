__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

import binascii
import os
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class UserApiKey(models.Model):
    """
    This model provide user API KEY to access API of healthsites
    """

    user = models.ForeignKey(User)
    api_key = models.CharField(
        max_length=40, primary_key=True)
    is_active = models.BooleanField(
        default=True)
    allow_write = models.BooleanField(
        default=False,
        help_text='allow this api key to write data')

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_key()
        return super(UserApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.api_key

    @staticmethod
    def get_user_api_key(user, autogenerate=False):
        """ return api key for user and autogenerate it

        :param user: user that going to be checked
        :type user: User

        :param autogenerate: flag for autogenerate if not found
        :type autogenerate: bool

        :return: List of api keys
        :rtype: list
        """
        api_keys = UserApiKey.objects.filter(
            user=user,
            is_active=True
        ).values_list('api_key', flat=True)
        if autogenerate and len(api_keys) == 0:
            UserApiKey.objects.create(
                user=user,
                is_active=True
            )
            api_keys = UserApiKey.get_user_api_key(user)

        return api_keys

    @staticmethod
    def get_user_from_api_key(api_key):
        """ return user from API Key

        :param api_key: user that going to be checked
        :type api_key: User

        :return: User found or None
        :rtype: User
        """
        try:
            api_key_user = UserApiKey.objects.get(
                api_key=api_key,
                is_active=True
            )
            return api_key_user.user
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
            api_key_user = UserApiKey.objects.get(
                api_key=api_key,
                is_active=True
            )
            return api_key_user
        except UserApiKey.DoesNotExist:
            return None
