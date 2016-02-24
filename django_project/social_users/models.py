# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import itertools
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Profile(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
            User, default=1)
    profile_picture = models.CharField(default="", max_length=150, blank=True)
    screen_name = models.CharField(default="", max_length=50, blank=True)
