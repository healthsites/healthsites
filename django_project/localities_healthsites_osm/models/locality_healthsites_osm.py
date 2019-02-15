__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '31/01/19'

from django.contrib.gis.db import models
from localities.models import Locality
from localities_osm.models.locality import LocalityOSMView

OSM_ELEMENT_TYPE = (
    ('node', 'node'),
    ('way', 'way'),
    ('relation', 'relation')
)


class LocalityHealthsitesOSM(models.Model):
    """ This model is a relationship of Locality Healthsites
    and locality OSM
    """
    healthsite = models.OneToOneField(Locality)
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

    class Meta:
        ordering = ('healthsite__name',)
        db_table = 'localities_healthsites_osm'

    def save(self, *args, **kwargs):
        # Create osm node if no osm id and pk found
        from localities_osm.models.locality import LocalityOSMNode
        from api.serializer.locality import LocalitySerializer
        if not self.osm_id and not self.osm_pk:
            node = LocalityOSMNode()
            node.geometry = self.healthsite.geom
            healthsite_data = LocalitySerializer(self.healthsite).data
            node.insert_healthsite_data(healthsite_data)
            node.save()
            self.osm_pk = node.pk
            self.osm_type = 'node'
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
