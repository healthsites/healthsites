# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

from django.contrib.gis.db import models
from .extension import LocalityOSMExtension  # noqa


class Tag(models.Model):
    """Model for tag not found in OSM."""

    extension = models.ForeignKey(
        LocalityOSMExtension,
        default=None, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=512)
    value = models.CharField(max_length=512)

    class Meta:
        ordering = ('name',)
        unique_together = ('extension', 'name')

    def __str__(self):
        return self.name
