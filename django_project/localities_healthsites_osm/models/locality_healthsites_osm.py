__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '31/01/19'

from django.contrib.gis.db import models
from django.db.utils import ConnectionDoesNotExist
from localities_osm.models.locality import LocalityOSMView, LocalityOSMNode
from localities_healthsites_osm.models.tag import Tag

OSM_ELEMENT_TYPE = (
    ('node', 'node'),
    ('way', 'way'),
    ('relation', 'relation')
)


class LocalityHealthsitesOSM(models.Model):
    """ This model is a relationship of Locality Healthsites
    and locality OSM
    """

    osm_id = models.BigIntegerField(
        db_index=True,
        null=True,
        blank=True
    )
    osm_pk = models.BigIntegerField(
        null=True,
        blank=True)
    osm_type = models.CharField(
        null=True,
        blank=True,
        choices=OSM_ELEMENT_TYPE,  # way / node / relation
        max_length=30)
    custom_tag = models.ManyToManyField(
        Tag,
        blank=True
    )

    class Meta:
        ordering = ('osm_id',)
        db_table = 'localities_healthsites_osm'
        verbose_name = 'Healthsites And Osm'
        verbose_name_plural = 'Healthsites And Osm'

    def save(self, *args, **kwargs):
        super(LocalityHealthsitesOSM, self).save(*args, **kwargs)

    def return_osm_view(self):
        if self.osm_id and self.osm_type:
            try:
                osm = LocalityOSMView.objects.get(
                    osm_id=self.osm_id,
                    osm_type=self.osm_type
                )
                return osm
            except LocalityOSMView.DoesNotExist:
                pass
        try:
            if self.pk:
                osms = LocalityOSMView.objects.filter(
                    row='%s-%s' % (self.osm_pk, self.osm_type)
                )
                if osms.count() > 0:
                    return osms[0]
        except LocalityOSMView.DoesNotExist:
            pass
        return None

    def return_osm_node(self):
        try:
            if self.osm_id and self.osm_type:
                try:
                    osm = LocalityOSMNode.objects.get(osm_id=self.osm_id)
                    return osm
                except LocalityOSMNode.DoesNotExist:
                    pass
            try:
                if self.pk:
                    return LocalityOSMNode.objects.get(pk=self.osm_pk)
            except LocalityOSMNode.DoesNotExist:
                pass
        except ConnectionDoesNotExist:
            pass
        return None
