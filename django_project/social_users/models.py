# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import itertools
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class UserDetail(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
        User, default=1)
    profile_picture = models.FileField(
        verbose_name='Profile Picture',
        help_text='Profile Picture',
        upload_to='profile_picture', default=None, blank=True, null=True)
