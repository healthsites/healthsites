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
    MANDATORY_FIELD = ['category', 'type', 'ownership', 'name', 'source']

    # mandatory
    osm_id = models.BigIntegerField()
    category = models.CharField(
        max_length=512, blank=True, null=True)
    type = models.CharField(
        max_length=512, blank=True, null=True)
    ownership = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(
        max_length=512, blank=True, null=True)
    source = models.CharField(
        max_length=512, blank=True, null=True)

    # optional
    operator = models.CharField(
        max_length=512, blank=True, null=True)
    physical_address = models.CharField(
        max_length=512, blank=True, null=True)
    contact_number = models.CharField(
        max_length=512, blank=True, null=True)
    status = models.CharField(
        max_length=512, blank=True, null=True)
    operation = models.CharField(
        max_length=512, blank=True, null=True)
    inpatient_service = models.CharField(
        max_length=512, blank=True, null=True)
    staff_doctors = models.CharField(
        max_length=512, blank=True, null=True)
    staff_nurses = models.CharField(
        max_length=512, blank=True, null=True)
    nature_of_facility = models.CharField(
        max_length=512, blank=True, null=True)
    insurance = models.CharField(
        max_length=512, blank=True, null=True)
    dispensing = models.CharField(
        max_length=512, blank=True, null=True)
    wheelchair_access = models.CharField(
        max_length=512, blank=True, null=True)
    emergency = models.CharField(
        max_length=512, blank=True, null=True)
    water_source = models.CharField(
        max_length=512, blank=True, null=True)
    power_source = models.CharField(
        max_length=512, blank=True, null=True)
    raw_data_archive_url = models.CharField(
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

    @staticmethod
    def get_count_of_basic(queryset):
        for mandatory_field in LocalityOSM.MANDATORY_FIELD:
            queryset = queryset.exclude(**{'%s' % mandatory_field: ''})
        return queryset.count()

    @staticmethod
    def get_count_of_complete(queryset):
        for field in LocalityOSM._meta.get_all_field_names():
            if field in ['osm_id', 'changeset_id', 'changeset_version', 'changeset_timestamp', 'changeset_user']:
                continue
            print field
            queryset = queryset.exclude(**{'%s' % field: ''})
        return queryset.count()

    def get_completeness(self):
        """ Get completeness of osm data
        :return: percentage of completeness
        :rtype: int
        """
        total = 0
        completed = 0
        for field in LocalityOSM._meta.get_all_field_names():
            total += 1
            if self._meta.get_field(field).get_internal_type() == 'CharField':
                if getattr(self, field):
                    completed += 1
        return float(completed * 100 / total)

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
    geometry = models.GeometryField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_way'
        verbose_name = 'OSM Way'
        verbose_name_plural = 'OSM Way'
