# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import itertools

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.gis.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey

from model_utils import FieldTracker
from pg_fts.fields import TSVectorField

from .querysets import PassThroughGeoManager, LocalitiesQuerySet


class ChangesetMixin(models.Model):
    changeset = models.ForeignKey('Changeset')
    version = models.IntegerField()

    class Meta:
        abstract = True

    def inc_version(self):
        self.version = (self.version or 0) + 1


class UpdateMixin(models.Model):
    class Meta:
        abstract = True

    def before_save(self, *args, **kwargs):
        """
        Executed before actually saving the model, should be overridden
        """
        pass

    def save(self, *args, **kwargs):
        # update
        if self.pk and not(kwargs.get('force_insert')):
            # execute any model specific changes
            self.before_save(*args, update=True, **kwargs)

            if self.tracker.changed():
                # increase version and save if there are more changed attrs
                self.inc_version()
                super(UpdateMixin, self).save(*args, **kwargs)
        # create
        else:
            self.before_save(*args, create=True, **kwargs)
            self.inc_version()
            super(UpdateMixin, self).save(*args, **kwargs)


class ArchiveMixin(ChangesetMixin):
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Domain(UpdateMixin, ChangesetMixin):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True, default='')
    template_fragment = models.TextField(null=True, blank=True, default='')

    attributes = models.ManyToManyField('Attribute', through='Specification')

    tracker = FieldTracker()

    def __unicode__(self):
        return u'{}'.format(self.name)


class DomainArchive(ArchiveMixin):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    template_fragment = models.TextField(null=True, blank=True)


class Locality(UpdateMixin, ChangesetMixin):
    domain = models.ForeignKey('Domain')
    uuid = models.TextField(unique=True)
    upstream_id = models.TextField(null=True, unique=True)
    geom = models.PointField(srid=4326)
    specifications = models.ManyToManyField('Specification', through='Value')

    objects = PassThroughGeoManager.for_queryset_class(LocalitiesQuerySet)()

    tracker = FieldTracker()

    def before_save(self, *args, **kwargs):
        # make sure that we don't allow uuid modifications
        if self.tracker.previous('uuid') and self.tracker.has_changed('uuid'):
            self.uuid = self.tracker.previous('uuid')

    def get_attr_map(self):
        return (
            self.domain.specification_set
            .order_by('id')
            .values('id', 'attribute__key')
        )

    def set_geom(self, lon, lat):
        self.geom.set_x(lon)
        self.geom.set_y(lat)

    def set_values(self, changed_data, social_user):
        attrs = self.get_attr_map()

        changed_values = []
        for key, data in changed_data.iteritems():
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
                if obj.tracker.changed():
                    obj.changeset = Changeset.objects.create(
                        social_user=social_user
                    )
                    obj.save()
                    changed_values.append((obj, _created))
                else:
                    # nothing changed, don't save the value
                    pass
            else:
                # attr_id was not found (maybe a bad attribute)
                LOG.warning(
                    'Locality %s has no attribute key %s', self.pk, key
                )

        # send values_updated signal
        signals.SIG_locality_values_updated.send(
            sender=self.__class__, instance=self
        )

        return changed_values

    def repr_dict(self):
        return {
            u'uuid': self.uuid,
            u'values': {
                val.specification.attribute.key: val.data
                for val in self.value_set.select_related('attribute').all()
            },
            u'geom': (self.geom.x, self.geom.y),
            u'version': self.version,
            u'changeset': self.changeset_id
        }

    def prepare_for_fts(self):
        data_values = itertools.groupby(
            self.value_set.order_by('specification__fts_rank')
            .values_list('specification__fts_rank', 'data'),
            lambda x: x[0]
        )

        return {k: ' '.join([x[1] for x in v]) for k, v in data_values}

    def __unicode__(self):
        return u'{}'.format(self.id)


class LocalityArchive(ArchiveMixin):
    """
    Archive for the Locality model
    """
    domain_id = models.IntegerField()
    uuid = models.TextField()
    upstream_id = models.TextField(null=True)
    geom = models.PointField(srid=4326)


class Value(UpdateMixin, ChangesetMixin):
    locality = models.ForeignKey('Locality')
    specification = models.ForeignKey('Specification')
    data = models.TextField(blank=True)

    tracker = FieldTracker()

    class Meta:
        unique_together = ('locality', 'specification')

    def __unicode__(self):
        return u'({}) {}={}'.format(
            self.locality.id, self.specification.attribute.key, self.data
        )


class ValueArchive(ArchiveMixin):
    """
    Archive for the Value model
    """
    locality_id = models.IntegerField()
    specification_id = models.IntegerField()
    data = models.TextField(blank=True)


class Attribute(UpdateMixin, ChangesetMixin):
    key = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True, default='')

    tracker = FieldTracker()

    def __unicode__(self):
        return u'{}'.format(self.key)

    def before_save(self, *args, **kwargs):
        # make sure key has a slug-like representation
        self.key = slugify(unicode(self.key)).replace('-', '_')


class AttributeArchive(ArchiveMixin):
    key = models.TextField()
    description = models.TextField(null=True, blank=True)


FTS_RANK = (
    ('A', 'Rank A'),
    ('B', 'Rank B'),
    ('C', 'Rank C'),
    ('D', 'Rank D')
)


class Specification(UpdateMixin, ChangesetMixin):
    domain = models.ForeignKey('Domain')
    attribute = models.ForeignKey('Attribute')
    required = models.BooleanField(default=False)
    fts_rank = models.CharField(max_length=1, default='D', choices=FTS_RANK)

    tracker = FieldTracker()

    class Meta:
        unique_together = ('domain', 'attribute')

    def __unicode__(self):
        return u'{} {}'.format(self.domain.name, self.attribute.key)


class SpecificationArchive(ArchiveMixin):
    """
    Archive for the Specification model

    We need to use simple IntegerFields instead of ForeignKey fields for
    relations as deletion of a related model triggers on_delete action, which
    can't preserve relation to a missing object.

    https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.ForeignKey.on_delete  # noqa
    """
    domain_id = models.IntegerField()
    attribute_id = models.IntegerField()
    required = models.BooleanField(default=False)
    fts_rank = models.CharField(max_length=1)


class Changeset(models.Model):
    social_user = models.ForeignKey(settings.AUTH_USER_MODEL)
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


class LocalityIndex(models.Model):
    locality = models.OneToOneField('Locality')
    ranka = models.TextField(null=True)
    rankb = models.TextField(null=True)
    rankc = models.TextField(null=True)
    rankd = models.TextField(null=True)
    fts_index = TSVectorField((
        ('ranka', 'A'), ('rankb', 'B'), ('rankc', 'C'), ('rankd', 'D')
    ))

# register signals
import signals  # noqa
