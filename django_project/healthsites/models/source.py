__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '21/09/23'

from django.contrib.gis.db import models

from localities_osm.models.base import LocalityOSMBase


class HealthsiteSource(LocalityOSMBase):
    """Healthsite source."""

    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    license = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )
