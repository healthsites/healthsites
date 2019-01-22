__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from django.contrib.gis.db import models
from localities.models import Locality

OSM_ELEMENT_TYPE = (
    ('node', 'node'),
    ('way', 'way'),
    ('relation', 'relation')
)


class LocalityHealthsitesOSM(models.Model):
    """ This model is a relationship of Locality Healthsites
    and locality OSM
    """
    healthsite = models.ForeignKey(Locality)
    osm_id = models.BigIntegerField(
        db_index=True
    )
    osm_type = models.CharField(
        choices=OSM_ELEMENT_TYPE,
        max_length=30)
    acceptance = models.BooleanField(
        default=False)

    class Meta:
        ordering = ('healthsite__name',)
        db_table = 'localities_healthsites_osm'
