# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import itertools
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class UserLink(models.Model):
    """
    List of user link
    """
    link = models.CharField(blank=True, default="", null=True,
                            max_length=200)

    def __str__(self):
        return self.link


class UserDetail(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(User, default=1)
    link = models.ForeignKey(UserLink, default=None, blank=True, null=True)
    profile_picture = models.FileField(
        verbose_name='Profile Picture',
        help_text='Profile Picture',
        upload_to='profile_picture', default=None, blank=True, null=True)
