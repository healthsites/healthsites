# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '26/04/19'

from django.conf import settings
from django.contrib.gis.db import models

OSM_ELEMENT_TYPE = (
    ('node', 'node'),
    ('way', 'way'),
    ('relation', 'relation')
)


class LocalityOSMExtension(models.Model):
    """Model for Locality OSM Extension."""

    osm_id = models.BigIntegerField(
        db_index=True,
        null=True,
        blank=True
    )
    osm_type = models.CharField(
        null=True,
        blank=True,
        choices=OSM_ELEMENT_TYPE,  # way / node / relation
        max_length=30)

    class Meta:
        ordering = ('osm_id',)
        unique_together = ('osm_id', 'osm_type')

    def save(self, *args, **kwargs):
        super(LocalityOSMExtension, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s/%s/%s' % (settings.OSM_API_URL, self.osm_type, self.osm_id)

    @staticmethod
    def get_extension_by_uuid(uuid):
        """ Return extension by checking uuid """
        from localities_osm_extension.models.tag import Tag
        try:
            return Tag.objects.get(name='uuid', value=uuid).extension
        except Tag.DoesNotExist:
            return None
