# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.gis.db import models


class ChangesetMixin(models.Model):
    changeset = models.ForeignKey('Changeset')
    version = models.IntegerField()

    class Meta:
        abstract = True

    def inc_version(self):
        self.version = (self.version or 0) + 1


class Domain(ChangesetMixin):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True, default='')
    template_fragment = models.TextField(null=True, blank=True, default='')

    attributes = models.ManyToManyField('Attribute', through='Specification')

    def __unicode__(self):
        return u'{}'.format(self.name)


class Locality(ChangesetMixin, models.Model):
    domain = models.ForeignKey('Domain')
    uuid = models.TextField(unique=True)
    upstream_id = models.TextField(null=True, unique=True)
    geom = models.PointField(srid=4326)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)
    specifications = models.ManyToManyField('Specification', through='Value')

    objects = models.GeoManager()

    def get_attr_map(self):
        return (
            self.domain.specification_set
            .order_by('id')
            .values('id', 'attribute__key')
        )

    def set_geom(self, lon, lat):
        self.geom.set_x(lon)
        self.geom.set_y(lat)

    def set_values(self, value_map, changeset):
        attrs = self.get_attr_map()

        changed_values = []
        for key, data in value_map.iteritems():
            # get attribute_id
            attr_list = [
                attr for attr in attrs if attr['attribute__key'] == key
            ]

            if attr_list:
                spec_id = attr_list[0]['id']
                # update or create new values
                try:
                    obj = self.value_set.get(specification_id=spec_id)
                    _created = False
                except Value.DoesNotExist:
                    obj = Value()
                    obj.locality = self
                    obj.specification_id = spec_id
                    _created = True

                obj.data = data
                obj.changeset = changeset
                # increase version number of a value
                obj.inc_version()
                obj.save()

                changed_values.append((obj, _created))
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

    def repr_simple(self):
        return {u'i': self.pk, u'g': [self.geom.x, self.geom.y]}

    def repr_dict(self):
        return {
            u'id': self.pk,
            u'uuid': self.uuid,
            u'values': {
                val.specification.attribute.key: val.data
                for val in self.value_set.select_related('attribute').all()
            },
            u'geom': [self.geom.x, self.geom.y]
        }

    def __unicode__(self):
        return u'{}'.format(self.id)


class Value(ChangesetMixin, models.Model):
    locality = models.ForeignKey('Locality')
    specification = models.ForeignKey('Specification')
    data = models.TextField(blank=True)

    class Meta:
        unique_together = ('locality', 'specification')

    def __unicode__(self):
        return u'({}) {}={}'.format(
            self.locality.id, self.specification.attribute.key, self.data
        )


class Attribute(ChangesetMixin, models.Model):
    key = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True, default='')

    def __unicode__(self):
        return u'{}'.format(self.key)

    def save(self, *args, **kwargs):
        # make sure key has a slug-like representation
        self.key = slugify(unicode(self.key)).replace('-', '_')

        super(Attribute, self).save(*args, **kwargs)


class Specification(ChangesetMixin, models.Model):
    domain = models.ForeignKey('Domain')
    attribute = models.ForeignKey('Attribute')
    required = models.BooleanField(default=False)

    class Meta:
        unique_together = ('domain', 'attribute')

    def __unicode__(self):
        return u'{} {}'.format(self.domain.name, self.attribute.key)


class Changeset(models.Model):
    # social_user = models.ForeignKey('SocialUser')
    created = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # update created and modified fields
        if self.pk and not(kwargs.get('force_insert')):
            super(Changeset, self).save(*args, **kwargs)
        else:
            self.created = timezone.now()
        super(Changeset, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.pk)
