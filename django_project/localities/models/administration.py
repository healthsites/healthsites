__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.gis.db import models


class Administrative(models.Model):
    """
    TODO:
      clean code, change all country references into using this
      because we added continent also and also maybe sub region,
      we need to change this as Administrative

    This is an administrative model (in abstract) that hold
    - code
    - name
    - polygon
    - in tree structure
    """
    id = models.AutoField(
        primary_key=True)

    name = models.CharField(
        verbose_name='',
        max_length=50,
        help_text='name of administrative')

    code = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        unique=True,
        help_text='administrative code')

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        help_text='is the administrative under other administrative (parent)',
        on_delete=models.SET_NULL)

    polygon_geometry = models.MultiPolygonField(
        srid=4326,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Country(Administrative):
    """Class for Country."""

    class Meta:
        """Meta Class"""
        verbose_name_plural = 'Countries'

    @property
    def get_codes(self):
        """ Return codes for the filters """
        if self.country_set.count() == 0:
            return [self.code]
        else:
            return list(self.country_set.values_list('code', flat=True))


Country._meta.get_field('name').verbose_name = 'Country name'
Country._meta.get_field('name').help_text = 'The name of the country.'
