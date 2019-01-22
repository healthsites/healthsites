__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from localities_osm.models.base import LocalityOSMBase
from localities_osm.querysets import (
    PassThroughGeoManager,
    OSMQuerySet
)


class LocalityOSM(LocalityOSMBase):
    osm_id = models.BigIntegerField()
    type = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(
        max_length=512, blank=True, null=True)
    emergency = models.CharField(
        max_length=512, blank=True, null=True)
    operator = models.CharField(
        max_length=512, blank=True, null=True)
    opening_hours = models.CharField(
        max_length=512, blank=True, null=True)
    contact_website = models.CharField(
        max_length=512, blank=True, null=True)
    contact_phone = models.CharField(
        max_length=512, blank=True, null=True)
    phone = models.CharField(
        max_length=512, blank=True, null=True)
    website = models.CharField(
        max_length=512, blank=True, null=True)
    speciality = models.CharField(
        max_length=512, blank=True, null=True)

    objects = PassThroughGeoManager.for_queryset_class(OSMQuerySet)()

    class Meta:
        abstract = True

    def __unicode__(self):
        if self.type:
            return u'%s [%s]' % (self.name, self.type)
        else:
            return u'%s' % self.name


class LocalityOSMView(LocalityOSM):
    """ This model is based on docker
    osm mode that created
    """
    geometry = models.GeometryField(
        srid=4326, blank=True, null=True)
    row = models.CharField(
        max_length=64, primary_key=True)
    osm_type = models.CharField(
        max_length=64, blank=True, null=True)
    objects = PassThroughGeoManager.for_queryset_class(OSMQuerySet)()

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities'


class LocalityOSMNode(LocalityOSM):
    """ This model is based on docker
    osm mode that created
    """
    geometry = models.PointField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_node'


class LocalityOSMWay(LocalityOSM):
    """ This model is based on docker
    osm mode that created
    """
    geometry = models.LineStringField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_way'
