__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.gis.db import models
from localities_osm.models.base import LocalityOSMBase
from localities_osm.querysets import OSMManager


class LocalityOSM(LocalityOSMBase):
    """
    This maps through to the docker-osm cache table containing healthcare facilities
    that defined in mapping.yml at docker-osm-healthcare/mapping.yml
    """
    MANDATORY_FIELD = ['amenity', 'healthcare', 'name', 'operator', 'source']

    # mandatory

    osm_id = models.BigIntegerField()
    amenity = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='amenity=clinic,doctors,hospital,dentist,pharmacy')
    healthcare = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='healthcare=doctor,pharmacy,hospital,clinic,'
                  'dentist,physiotherapist,alternative'
                  ',laboratory,optometrist,rehabilitation,'
                  'blood_donation,birthing_center')
    name = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='name')
    operator = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='operator')
    source = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='source')

    # OPTIONAL
    speciality = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='healthcare:speciality')
    operator_type = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='operator:type=public,private,community,religious,government,ngo')
    contact_number = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='contact:phone')
    operational_status = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='operational_status')
    opening_hours = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='opening_hours')
    beds = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='beds')
    staff_doctors = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='staff_count:doctors')
    staff_nurses = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='staff_count:nurses')
    health_amenity_type = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='health_amenity:type')
    dispensing = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='dispensing (boolean value)')
    wheelchair = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='wheelchair (boolean value)')
    emergency = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='emergency (boolean value)')
    insurance = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='insurance:health')
    water_source = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='water_source')
    electricity = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='electricity')
    is_in_health_area = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='is_in:health_area')
    is_in_health_zone = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='is_in:health_zone')
    url = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='url')

    addr_housenumber = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='addr:housenumber')
    addr_street = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='addr:street')
    addr_postcode = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='addr:postcode')
    addr_city = models.CharField(
        max_length=512, blank=True, null=True,
        help_text='addr:city')

    # changesets
    changeset_id = models.IntegerField(blank=True, null=True)
    changeset_version = models.IntegerField(blank=True, null=True)
    changeset_timestamp = models.DateTimeField(blank=True, null=True)
    changeset_user = models.CharField(
        max_length=512, blank=True, null=True)

    objects = OSMManager()

    class Meta:
        abstract = True

    def __str__(self):
        if self.amenity:
            return u'%s [%s]' % (self.name, self.amenity)
        else:
            return u'%s' % self.name

    @staticmethod
    def get_count_of_basic(queryset):
        for mandatory_field in LocalityOSM.MANDATORY_FIELD:
            queryset = queryset.exclude(**{'%s' % mandatory_field: ''})
        return queryset.count()

    @staticmethod
    def get_count_of_complete(queryset):
        for meta_field in LocalityOSM._meta.get_fields():
            field = meta_field.name
            if field in [
                'osm_id', 'changeset_id', 'changeset_version',
                'changeset_timestamp', 'changeset_user']:
                continue
            queryset = queryset.exclude(**{'%s' % field: ''})
        return queryset.count()

    def get_completeness(self):
        """ Get completeness of osm data
        :return: percentage of completeness
        :rtype: int
        """
        total = 0
        completed = 0
        for meta_field in LocalityOSM._meta.get_fields():
            field = meta_field.name
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


class LocalityOSMExtra(LocalityOSMBase):
    # Administrative code
    administrative_code = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        help_text='Administrative code'
    )

    class Meta:
        abstract = True


class LocalityOSMView(LocalityOSM, LocalityOSMExtra):
    """ This model is a view model (that created on migrations) that
    union node and way
    """
    NODE = 'node'
    WAY = 'way'

    row = models.CharField(
        max_length=64, primary_key=True)
    geometry = models.GeometryField(
        srid=4326, blank=True, null=True)
    osm_type = models.CharField(
        max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities'
        verbose_name = 'OSM Node and Way'
        verbose_name_plural = 'OSM Node and Way'


class LocalityOSMNode(LocalityOSM, LocalityOSMExtra):
    """ This model is based on docker osm node
    """
    geometry = models.PointField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_node'
        verbose_name = 'OSM Node'
        verbose_name_plural = 'OSM Node'


class LocalityOSMWay(LocalityOSM, LocalityOSMExtra):
    """ This model is based on docker osm way
    """
    geometry = models.GeometryField(
        srid=4326, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osm_healthcare_facilities_way'
        verbose_name = 'OSM Way'
        verbose_name_plural = 'OSM Way'
