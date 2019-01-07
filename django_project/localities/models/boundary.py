# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models


# -------------------------------------------------
# BOUNDARY OF COUNTRY
# -------------------------------------------------
class Boundary(models.Model):
    """This is an abstract model that vectors can inherit from. e.g. country"""
    name = models.CharField(
        verbose_name='',
        help_text='',
        max_length=50,
        null=False,
        blank=False)

    polygon_geometry = models.MultiPolygonField(
        srid=4326)

    id = models.AutoField(
        primary_key=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Country(Boundary):
    """Class for Country."""

    class Meta:
        """Meta Class"""
        verbose_name_plural = 'Countries'


Country._meta.get_field('name').verbose_name = 'Country name'
Country._meta.get_field('name').help_text = 'The name of the country.'
