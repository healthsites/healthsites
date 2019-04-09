__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from localities_osm.models.base import LocalityOSMBase
from localities_osm.querysets import (
    PassThroughGeoManager,
    OSMQuerySet
)


class LocalityOSM(LocalityOSMBase):
    """ This maps through to the docker-osm cache table containing healthcare facilities
    that defined in mapping.yml at docker-osm-healthcare/mapping.yml
    """
    osm_id = models.BigIntegerField()
    type = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(
        max_length=512, blank=True, null=True)
    physical_address = models.CharField(
        max_length=512, blank=True, null=True)
    phone = models.CharField(
        max_length=512, blank=True, null=True)
    nature_of_facility = models.CharField(
        max_length=512, blank=True, null=True)
    scope_of_service = models.CharField(
        max_length=512, blank=True, null=True)
    operation = models.CharField(
        max_length=512, blank=True, null=True)
    full_time_beds = models.CharField(
        max_length=512, blank=True, null=True)
    nurses = models.CharField(
        max_length=512, blank=True, null=True)
    doctors = models.CharField(
        max_length=512, blank=True, null=True)
    ownership = models.CharField(
        max_length=512, blank=True, null=True)
    operator = models.CharField(
        max_length=512, blank=True, null=True)
    status = models.CharField(
        max_length=512, blank=True, null=True)
    emergency = models.CharField(
        max_length=512, blank=True, null=True)
    website = models.CharField(
        max_length=512, blank=True, null=True)
    speciality = models.CharField(
        max_length=512, blank=True, null=True)

    # changesets
    changeset_id = models.IntegerField(blank=True, null=True)
    changeset_version = models.IntegerField(blank=True, null=True)
    changeset_timestamp = models.DateTimeField(blank=True, null=True)
    changeset_user = models.CharField(
        max_length=512, blank=True, null=True)

    objects = PassThroughGeoManager.for_queryset_class(OSMQuerySet)()

    class Meta:
        abstract = True

    def __unicode__(self):
        if self.type:
            return u'%s [%s]' % (self.name, self.type)
        else:
            return u'%s' % self.name

    def insert_healthsite_data(self, healthsite_data):
        attributes = healthsite_data['attributes']
        try:
            attributes.update(attributes['inpatient_service'])
        except KeyError:
            pass
        try:
            attributes.update(attributes['staff'])
        except KeyError:
            pass
        for key, value in attributes.items():
            setattr(self, key, value)


class LocalityOSMView(LocalityOSM):
    """ This model is a view model (that created on migrations) that
    union node and way
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
        verbose_name = 'OSM Node and Way'
        verbose_name_plural = 'OSM Node and Way'


class LocalityOSMNode(LocalityOSM):
    """ This model is based on docker osm node
    """
    geometry = models.PointField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_node'
        verbose_name = 'OSM Node'
        verbose_name_plural = 'OSM Node'


class LocalityOSMWay(LocalityOSM):
    """ This model is based on docker osm way
    """
    geometry = models.LineStringField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_way'
        verbose_name = 'OSM Way'
        verbose_name_plural = 'OSM Way'
