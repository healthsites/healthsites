import logging
LOG = logging.getLogger(__name__)

from django.utils import timezone

from django.contrib.gis.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default='')

    def __unicode__(self):
        return u'{}'.format(self.name)


class Locality(models.Model):
    group = models.ForeignKey('Group')
    uuid = models.TextField(unique=True)
    upstream_id = models.TextField(null=True)
    geom = models.PointField(srid=4326)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)
    attributes = models.ManyToManyField('Attribute', through='Value')

    def save(self, *args, **kwargs):
        # update created and modified fields
        if self.pk:
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

    def __unicode__(self):
        return u'({}) {}={}'.format(
            self.locality.id, self.attribute.name, self.value
        )


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default='')

    in_group = models.ManyToManyField('Group')

    def __unicode__(self):
        return u'{}'.format(self.name)
