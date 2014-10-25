import logging
LOG = logging.getLogger(__name__)

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.gis.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default='')

    def __unicode__(self):
        return u'{}'.format(self.name)


class Locality(models.Model):
    group = models.ForeignKey('Group')
    uuid = models.TextField(unique=True)
    upstream_id = models.TextField(null=True, unique=True)
    geom = models.PointField(srid=4326)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)
    attributes = models.ManyToManyField('Attribute', through='Value')

    objects = models.GeoManager()

    def get_attr_map(self):
        return (
            Attribute.objects
            .filter(in_groups=self.group)
            .order_by('id')
            .values('id', 'key')
        )

    def set_values(self, value_map):
        attrs = self.get_attr_map()
        changed_values = []
        for key, data in value_map.iteritems():
            # get attribute_id
            attr_list = [attr for attr in attrs if attr['key'] == key]

            if attr_list:
                attr_id = attr_list[0]['id']
                # update or create new values
                changed_values.append(
                    self.value_set.update_or_create(
                        data=data, attribute_id=attr_id
                    )
                )
            else:
                # attr_id was not found (maybe a bad attribute)
                LOG.warning(
                    'Locality %s has no attribute key %s', self.pk, key
                )

        return changed_values

    def save(self, *args, **kwargs):
        # update created and modified fields
        if self.pk and not(kwargs.get('force_insert')):
            self.modified = timezone.now()
        else:
            current_time = timezone.now()
            self.modified = current_time
            self.created = current_time
        super(Locality, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.id)


class Value(models.Model):
    locality = models.ForeignKey('Locality')
    attribute = models.ForeignKey('Attribute')
    data = models.TextField(blank=True)

    class Meta:
        unique_together = ('locality', 'attribute')

    def __unicode__(self):
        return u'({}) {}={}'.format(
            self.locality.id, self.attribute.key, self.data
        )


class Attribute(models.Model):
    key = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True, default='')

    in_groups = models.ManyToManyField('Group')

    def __unicode__(self):
        return u'{}'.format(self.key)

    def save(self, *args, **kwargs):
        # make sure key has a slug-like representation
        self.key = slugify(unicode(self.key))

        super(Attribute, self).save(*args, **kwargs)
