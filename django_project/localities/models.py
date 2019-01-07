# -*- coding: utf-8 -*-
import itertools
import logging
LOG = logging.getLogger(__name__)
from datetime import datetime


from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from django.utils.text import slugify

from model_utils import FieldTracker

from .querysets import LocalitiesQuerySet, PassThroughGeoManager
from .variables import attributes_availables

LOG = logging.getLogger(__name__)









































# register signals
from . import signals  # noqa  # isort:skip
