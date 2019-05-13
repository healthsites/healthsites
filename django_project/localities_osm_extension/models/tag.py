# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

from django.contrib.gis.db import models
from localities_osm_extension.models.extension import LocalityOSMExtension


class Tag(models.Model):
    """Model for tag not found in OSM."""

    extension = models.ForeignKey(
        LocalityOSMExtension,
        default=None)
    name = models.CharField(max_length=512)
    value = models.CharField(max_length=512)

    class Meta:
        ordering = ('name',)
        unique_together = ('extension', 'name')

    def __unicode__(self):
        return self.name
