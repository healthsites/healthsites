# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

from django.contrib.gis.db import models


class Tag(models.Model):
    """Model for tag not found in OSM."""

    name = models.CharField(max_length=512, blank=False, null=False)
    value = models.CharField(max_length=512, blank=False, null=False)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name
