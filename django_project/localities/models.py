# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import itertools
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from model_utils import FieldTracker
from pg_fts.fields import TSVectorField
from .querysets import PassThroughGeoManager, LocalitiesQuerySet
from django.db.models.signals import post_save


class ChangesetMixin(models.Model):
    """
    This mixin facilitates defines common attributes and methods for models
    that will record and track changes
    """

    changeset = models.ForeignKey('Changeset')
    version = models.IntegerField()

    class Meta:
        abstract = True

    def inc_version(self):
        """
        Common method to increase version of a tracked object
        """

        self.version = (self.version or 0) + 1


class UpdateMixin(models.Model):
    """
    This mixin defines common methods for models that are tracked using
    changeset and version

    *save* method will increase version of an 'object' if there are changes

    Models that use this mixin should be extra careful when overriding save,
    in case they just need to change some fields, 'before_save' should be
    overridden instead
    """

    class Meta:
        abstract = True

    def before_save(self, *args, **kwargs):
        """
        Executed before actually saving the model, should be overridden
        """

        pass

    def save(self, *args, **kwargs):
        # object exists - update
        if self.pk and not (kwargs.get('force_insert')):
            # execute any model specific changes
            self.before_save(*args, update=True, **kwargs)

            if self.tracker.changed():
                # increase version and save in case there are changed attrs
                self.inc_version()
                super(UpdateMixin, self).save(*args, **kwargs)
        # object does not exist - create
        else:
            self.before_save(*args, create=True, **kwargs)
            self.inc_version()
            super(UpdateMixin, self).save(*args, **kwargs)


class ArchiveMixin(ChangesetMixin):
    """
    This mixin defines common attributes for Object archival

    We opted to use ContentType framework in order to delete referenced
    objects without depending on *on_delete* support in Django

    Object archival is facilitated by Django signal framework
    """

    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Domain(UpdateMixin, ChangesetMixin):
    """
    Domain defines a common theme for the data, for example: Health,
    Sanitation and House, might be considered as unique domains

    Domain is defined by a *name* and an optional *description*. Every domain
    might have different attributes so we can define it's representation using
    the *template_fragment*.

    Connection between a Domain and Attributes is defined though the
    *Specification* model
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True, default='')
    template_fragment = models.TextField(null=True, blank=True, default='')

    attributes = models.ManyToManyField('Attribute', through='Specification')

    tracker = FieldTracker()

    def __unicode__(self):
        return u'{}'.format(self.name)


class DomainArchive(ArchiveMixin):
    """
    Archive model for the Domain
    """

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    template_fragment = models.TextField(null=True, blank=True)


class Locality(UpdateMixin, ChangesetMixin):
    """
    A Locality is uniquely defined by an *uuid* attribute. Attribute *geom*
    stores geometry as a point object. *upstream_id* is used to preserve link
    to the originating dataset which is used to find and update a Locality on
    any reoccurring data imports.

    A Locality is in a *Domain* and data values for Attributes, to be exact,
    their Specifications, are defined through *Value*
    """

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

    def _get_attr_map(self):
        return (
            self.domain.specification_set
                .order_by('id')
                .values('id', 'attribute__key')
        )

    def set_geom(self, lon, lat):
        """
        Helper method to set Locality geometry
        """

        self.geom.set_x(lon)
        self.geom.set_y(lat)

    def set_values(self, changed_data, social_user, changeset=None):
        """
        Set values for a Locality which are defined by Specifications

        Once all of values are set, 'SIG_locality_values_updated' signal will
        be triggered to update FullTextSearch index for this Locality
        """
        special_key = ['scope_of_service', "ancillary_services", "activities", "inpatient_service", "staff"]
        attrs = self._get_attr_map()

        tmp_changeset = changeset

        changed_values = []
        for key, data in changed_data.iteritems():
            if key in special_key:
                data = data.replace(",", "|")
                data = data.replace("| ", "|")
            # try to match key from changed items with a key from attr_map
            attr_list = [
                attr for attr in attrs if attr['attribute__key'] == key
                ]

            if attr_list:
                # get specification id for specific key
                spec_id = attr_list[0]['id']

                # update or create new values
                try:
                    obj = self.value_set.get(specification_id=spec_id)
                    _created = False
                except Value.DoesNotExist:
                    # in case there is no value for the specification, create
                    obj = Value()
                    obj.locality = self
                    obj.specification_id = spec_id
                    _created = True

                # set data
                obj.data = data

                # check if Value.data actually changed, and save if it did
                if obj.tracker.changed():
                    if not (tmp_changeset):
                        tmp_changeset = Changeset.objects.create(
                                social_user=social_user
                        )
                    obj.changeset = tmp_changeset
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
        """
        Basic locality representation, as a dictionary
        """

        return {
            u'uuid': self.uuid,
            u'values': {
                val.specification.attribute.key: val.data
                for val in self.value_set.select_related().exclude(data__isnull=True).exclude(data__exact='')
                },
            u'geom': (self.geom.x, self.geom.y),
            u'version': self.version,
            u'changeset': self.changeset_id
        }

    def is_type(self, value):
        if value != "":
            try:
                self.value_set.filter(specification__attribute__key='type').get(data=value)
                return True
            except Exception as e:
                return False
        return True

    def prepare_for_fts(self):
        """
        Retrieve and group *Value* objects, for this Locality, based on their
        FTS ordering (defined by *Specification*)
        """

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
    Archive model for the Locality

    We need to use simple IntegerFields instead of ForeignKey fields for
    relations as deletion of a related model triggers on_delete action, which
    can't preserve relation to a missing object.

    https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.ForeignKey.on_delete  # noqa
    """

    domain_id = models.IntegerField()
    uuid = models.TextField()
    upstream_id = models.TextField(null=True)
    geom = models.PointField(srid=4326)


class Value(UpdateMixin, ChangesetMixin):
    """
    *Value* is the link between a *Locality*, *Specification* and it's *data*

    All of the attributes are stored as textual data
    """

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
    """
    An Attribute is defined by a *key* and an optional *description*.

    An Attribute can be a part of multiple Domains and it's behaviour can be
    altered through *Specification* for a specific *Domain*.
    """

    key = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True, default='')

    tracker = FieldTracker()

    def __unicode__(self):
        return u'{}'.format(self.key)

    def before_save(self, *args, **kwargs):
        # make sure key has a slug-like representation
        self.key = slugify(unicode(self.key)).replace('-', '_')


class AttributeArchive(ArchiveMixin):
    """
    Archive for the Attribute model
    """

    key = models.TextField()
    description = models.TextField(null=True, blank=True)


# constant FTS ranks
FTS_RANK = (
    ('A', 'Rank A'),
    ('B', 'Rank B'),
    ('C', 'Rank C'),
    ('D', 'Rank D')
)


class Specification(UpdateMixin, ChangesetMixin):
    """
    A Specification in an specialization of an Attribute for a particular
    Domain. Specification defines *required* and *fts_rank* fields.

    *required* - defines if an Attribute is mandatory for a Domain
    *fts_rank* - priority for the FTS index, from the, highest, 'A' through 'D'

    """

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
    """

    domain_id = models.IntegerField()
    attribute_id = models.IntegerField()
    required = models.BooleanField(default=False)
    fts_rank = models.CharField(max_length=1)


class Changeset(models.Model):
    """
    Changeset stores information about time of change *created* and user which
    created the change *social_user*. Optional *comment* field might be used
    to store more information about the context of the change
    """

    social_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Update created field when creating a new changeset, on update don't
        change anything
        """

        if self.pk and not (kwargs.get('force_insert')):
            super(Changeset, self).save(*args, **kwargs)
        else:
            self.created = timezone.now()
        super(Changeset, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.pk)


class LocalityIndex(models.Model):
    """
    LocalityIndex enables FullTextSearch filtering for the *Locality* based on
    its *Values* and *fts_rank* specified by a *Specification*

    LocalityIndex will be autoupdated when 'SIG_locality_values_updated' is
    triggered
    """

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
from .tasks import load_data_task


class DataLoader(models.Model):
    """
    """
    REPLACE_DATA_CODE = 1
    UPDATE_DATA_CODE = 2

    DATA_LOADER_MODE_CHOICES = (
        (REPLACE_DATA_CODE, 'Replace Data'),
        (UPDATE_DATA_CODE, 'Update Data')
    )

    COMMA_CHAR = ','
    TAB_CHAR = '\t'

    COMMA_CODE = 1  # ,
    TAB_CODE = 2  # \t

    SEPARATORS = {
        COMMA_CODE: COMMA_CHAR,
        TAB_CODE: TAB_CHAR
    }

    SEPARATOR_CHOICES = (
        (COMMA_CODE, 'Comma'),
        (TAB_CODE, 'Tab'),
    )

    organisation_name = models.CharField(
            verbose_name='Organization\'s Name',
            help_text='Organization\'s Name',
            null=False,
            blank=False,
            max_length=100
    )

    json_concept_mapping = models.FileField(
            verbose_name='JSON Concept Mapping',
            help_text='JSON Concept Mapping File.',
            upload_to='json_mapping/%Y/%m/%d',
            max_length=100
    )

    csv_data = models.FileField(
            verbose_name='CSV Data',
            help_text='CSV data that contains the data.',
            upload_to='csv_data/%Y/%m/%d',
            max_length=100
    )

    data_loader_mode = models.IntegerField(
            choices=DATA_LOADER_MODE_CHOICES,
            verbose_name="Data Loader Mode",
            help_text='The mode of the data loader.',
            blank=False,
            null=False
    )

    applied = models.BooleanField(
            verbose_name='Applied',
            help_text='Whether the data update has been applied or not.',
            default=False
    )

    author = models.ForeignKey(
            User,
            verbose_name='Author',
            help_text='The user who propose the data loader.',
            null=False
    )

    date_time_uploaded = models.DateTimeField(
            verbose_name='Uploaded (time)',
            help_text='Timestamp (UTC) when the data uploaded',
            null=False,
    )

    date_time_applied = models.DateTimeField(
            verbose_name='Applied (time)',
            help_text='When the data applied (loaded)',
            null=True
    )

    separator = models.IntegerField(
            choices=SEPARATOR_CHOICES,
            verbose_name="Separator Character",
            help_text='Separator character.',
            null=False,
            default=COMMA_CODE
    )

    notes = models.TextField(
            verbose_name='Notes',
            help_text='Notes',
            null=True,
            blank=True,
            default=''
    )

    def __str__(self):
        return self.organisation_name

    def save(self, *args, **kwargs):
        if not self.date_time_uploaded:
            self.date_time_uploaded = datetime.utcnow()
        super(DataLoader, self).save(*args, **kwargs)


# method for updating
def load_data(sender, instance, **kwargs):
    if not instance.applied:
        load_data_task.delay(instance.pk)


# register the signal
post_save.connect(load_data, sender=DataLoader)


# -------------------------------------------------
# BOUNDARY OF COUNTRY
# -------------------------------------------------
class Boundary(models.Model):
    """This is an abstract model that vectors can inherit from. e.g. country"""
    name = models.CharField(
            verbose_name='',
            help_text='',
            max_length=50,
            null=False,
            blank=False)

    polygon_geometry = models.MultiPolygonField(
            srid=4326)

    id = models.AutoField(
            primary_key=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Country(Boundary):
    """Class for Country."""

    class Meta:
        """Meta Class"""
        verbose_name_plural = 'Countries'


Country._meta.get_field('name').verbose_name = 'Country name'
Country._meta.get_field('name').help_text = 'The name of the country.'
