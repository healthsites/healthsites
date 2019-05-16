# -*- coding: utf-8 -*-
import itertools
import json
import logging
from datetime import datetime

from pg_fts.fields import TSVectorField

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from django.utils.text import slugify

from model_utils import FieldTracker

from .querysets import LocalitiesQuerySet, PassThroughGeoManager
from .variables import attributes_availables

LOG = logging.getLogger(__name__)


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
    DEFINED_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    domain = models.ForeignKey('Domain')
    uuid = models.TextField(unique=True)
    upstream_id = models.TextField(null=True, unique=True)
    geom = models.PointField(srid=4326)
    specifications = models.ManyToManyField('Specification', through='Value')
    name = models.TextField()
    source = models.TextField(default='healthsites.io')
    migrated = models.BooleanField(default=False)

    # completeness is a big calculation
    # so it has to be an field
    completeness = models.FloatField(null=True, default=0.0)
    is_master = models.BooleanField(default=True)

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
        special_key = [
            'scope_of_service', 'ancillary_services', 'activities', 'inpatient_service', 'staff'
        ]
        attrs = self._get_attr_map()

        tmp_changeset = changeset

        changed_values = []
        for key, data in changed_data.iteritems():
            if key in special_key:
                data = data.replace(',', '|')
                data = data.replace('| ', '|')
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

        # calculate completeness
        if changed_values:
            self.completeness = self.calculate_completeness()
            self.save()

        return changed_values

    def repr_dict(self, clean=False, in_array=False):
        """
        Basic locality representation, as a dictionary
        """

        dict = {
            u'uuid': self.uuid,
            u'upstream': self.upstream_id,
            u'source': self.source,
            u'name': self.name,
            u'geom': (self.geom.x, self.geom.y),
            u'version': self.version,
            u'date_modified': self.changeset.created,
            u'completeness': '%s%%' % format(self.completeness, '.2f'),
        }

        dict['values'] = {}

        data_query = (
            self.value_set.select_related().exclude(data__isnull=True).exclude(data__exact='')
        )

        for val in data_query:
            if in_array:
                dict['values'][val.specification.attribute.key] = [
                    data for data in val.data.split('|') if data]

                clean_data = dict['values'][val.specification.attribute.key]
                if len(clean_data) == 0:
                    dict['values'][val.specification.attribute.key] = '-'
                elif len(clean_data) == 1:
                    dict['values'][val.specification.attribute.key] = clean_data[0]
                continue
            if clean:
                # clean if empty
                temp = val.data.replace('|', '')
                if len(temp) == 0:
                    val.data = ''
                # clean data
                val.data = val.data.replace('|', ',')
                val.specification.attribute.key = (
                    val.specification.attribute.key.replace('_', '-')
                )
                cleaned_data = val.data.replace(',', '')
                if len(cleaned_data) > 0:
                    dict['values'][val.specification.attribute.key] = val.data
            else:
                dict['values'][val.specification.attribute.key] = val.data

        try:
            site = Site.objects.get(name=dict[u'source'])
            dict[u'source_url'] = site.domain
        except Site.DoesNotExist:
            pass

        # exclusive for open street map
        if self.upstream_id is not None and 'openstreetmap' in self.upstream_id.lower():
            osm_whole_id = self.upstream_id.split(u'¶')
            if len(osm_whole_id) > 0:
                osm_whole_id = osm_whole_id[1]
                identifier = osm_whole_id[0]
                osm_id = osm_whole_id[1:]
                if identifier == 'n':
                    dict['osm_type'] = 'node'
                    url = 'http://www.openstreetmap.org/node/' + osm_id
                elif identifier == 'r':
                    dict['osm_type'] = 'relation'
                    url = 'http://www.openstreetmap.org/relation/' + osm_id
                elif identifier == 'w':
                    dict['osm_type'] = 'way'
                    url = 'http://www.openstreetmap.org/way/' + osm_id

                if url:
                    dict['osm_id'] = osm_id
                    dict['source_url'] = url
        return dict

    def is_type(self, value):
        if value != '':
            try:
                self.value_set.filter(specification__attribute__key='type').get(data=value)
                return True
            except Exception:
                return False
        return True

    def calculate_completeness(self):
        DEFAULT_VALUE = 4  # GUID & GEOM & NAME & DATA SOURCE
        global_attr = attributes_availables['global']
        specific_attr = attributes_availables['hospital']
        for key in attributes_availables.keys():
            try:
                self.value_set.filter(specification__attribute__key='type').get(
                    data__icontains=key
                )
                specific_attr = attributes_availables[key]
            except Value.DoesNotExist:
                continue

        values = self.repr_dict()['values']
        counted_value = DEFAULT_VALUE
        max_value = len(global_attr) + len(specific_attr) + DEFAULT_VALUE

        for attr in global_attr + specific_attr:
            if attr in values:
                data = values[attr]
                if len(data.replace('-', '').replace('|', '').strip()) != 0:
                    counted_value += 1

        return (counted_value + 0.0) / (max_value + 0.0) * 100

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

    def update_what3words(self, user, changeset):
        from utils import get_what_3_words
        what3words = get_what_3_words(self.geom)
        if what3words != '':
            self.set_values({'what3words': what3words}, user, changeset)

    def get_synonyms(self):
        synonyms = SynonymLocalities.objects.get(locality=self)
        return synonyms

    def __unicode__(self):
        return u'{}'.format(self.id)

    def validate_data_by_defined_list(self, data, key, options, required=False):
        """ Check value data by key if it is string and it is in options.

        :param data: Data to be inserted
        :param key: Key data that is checked
        :param options: Options to be checked
        :return:
        """
        try:
            value = data[key]
            if isinstance(value, list):
                raise ValueError(
                    'nature_of_facility should be string'
                )
            if value not in options:
                raise ValueError(
                    '%s is not recognized, options : %s' % (key, options)
                )

        except KeyError as e:
            if required:
                raise ValueError('%s is required' % e)
            pass

    def validate_data(self, data):
        """ Validate data based on fields

        :param data: Data that will be inserted
        :type data: dict
        """
        try:
            data['lng'] = float(data['lng'])
        except ValueError:
            raise ValueError('lng is not in float')
        try:
            data['lat'] = float(data['lat'])
        except ValueError:
            raise ValueError('lat is not in float')

        if not data['name']:
            raise ValueError('name is empty')

        domain = Domain.objects.get(name='Health')
        attributes = Specification.objects.filter(domain=domain).filter(required=True)
        for attribute in attributes:
            if not data[attribute.attribute.key]:
                raise ValueError('%s is empty' % attribute.attribute.key)

        # inpatient_service
        try:
            inpatient_service = data['inpatient_service']
            try:
                full_time_beds = inpatient_service['full_time_beds']
            except KeyError:
                raise ValueError(
                    'full_time_beds needs to be in inpatient_service'
                )
            try:
                part_time_beds = inpatient_service['part_time_beds']
            except KeyError:
                raise ValueError(
                    'part_time_beds needs to be in inpatient_service'
                )
            data['inpatient_service'] = '%s|%s' % (
                full_time_beds,
                part_time_beds
            )
        except KeyError:
            pass

        # staff
        try:
            staff = data['staff']
            try:
                doctors = staff['doctors']
            except KeyError:
                raise ValueError(
                    'doctors needs to be in staff'
                )
            try:
                nurses = staff['nurses']
            except KeyError:
                raise ValueError(
                    'nurses needs to be in staff'
                )
            data['staff'] = '%s|%s' % (
                doctors,
                nurses
            )
        except KeyError:
            pass

        # nature of facility
        options = ['clinic without beds',
                   'clinic with beds',
                   'first referral hospital',
                   'second referral hospital or General hospital',
                   'tertiary level including University hospital']
        self.validate_data_by_defined_list(
            data, 'nature_of_facility', options)

        # nature of facility
        options = ['public',
                   'private not for profit',
                   'private commercial']
        self.validate_data_by_defined_list(
            data, 'ownership', options)

        # defined_hours
        try:
            defined_hours = []
            for index, day in enumerate(Locality.DEFINED_DAYS):
                try:
                    hours = data['defining_hours'][day]
                    if isinstance(hours, str) or isinstance(hours, unicode):
                        if hours == '':
                            hours = []
                        else:
                            try:
                                hours = json.loads(hours)
                            except ValueError:
                                pass
                    if not isinstance(hours, list):
                        raise ValueError('%s is need to be in list' % day)
                    if len(hours) == 1:
                        hours.append('-')
                    elif len(hours) > 2:
                        raise ValueError('maximum lenght of %s is 2' % day)
                    hours = '-'.join(hours)
                    if not hours:
                        hours = '-'
                    defined_hours.append(hours)
                except KeyError as e:
                    raise ValueError('%s is required on defined_hours' % e)
            data['defining_hours'] = defined_hours
        except KeyError:
            pass
        except TypeError:
            raise TypeError('defining_hours needs to be in dictionary')

        return True

    def update_data(self, data, user):
        """ Update locality data with new data.

        :param data: Data that will be inserted
        :type data: dict
        """
        import uuid
        from django.contrib.gis.geos import Point
        from localities.tasks import regenerate_cache, regenerate_cache_cluster

        self.validate_data(data)
        old_geom = None
        try:
            old_geom = [self.geom.x, self.geom.y]
            self.set_geom(data['lng'], data['lat'])
        except AttributeError:
            self.geom = Point(data['lng'], data['lat'])

        self.name = data['name']

        # there are some changes so create a new changeset
        changeset = Changeset.objects.create(
            social_user=user
        )
        self.changeset = changeset

        del data['lng']
        del data['lat']

        created = False
        if not self.pk:
            created = True
            self.domain = Domain.objects.get(name='Health')
            self.changeset = changeset
            self.uuid = uuid.uuid4().hex
            self.upstream_id = u'web¶{}'.format(self.uuid)
            self.save()

        self.set_specifications(data, changeset)
        if not created and self.tracker.changed():
            self.changeset = changeset
            self.save()

        # generate some attributes if location changed/created
        new_geom = [self.geom.x, self.geom.y]
        if new_geom != old_geom or created:
            try:
                self.update_what3words(user, changeset)
            except AttributeError:
                pass
            regenerate_cache_cluster.delay()
        regenerate_cache.delay(changeset.pk, self.pk)
        return True

    def set_specifications(
            self, data, changeset, autocreate_specification=True):
        """
        Set values for a Locality which are defined by Specifications

        Once all of values are set, 'SIG_locality_values_updated' signal will
        be triggered to update FullTextSearch index for this Locality

        :param data: Data to be inserted as specification
        :type data: dict
        """
        fields = self._meta.get_all_field_names()
        domain = Domain.objects.get(name='Health')

        changed_values = []
        for key, value in data.iteritems():
            if key in fields:
                continue

            if isinstance(value, list):
                value = '|'.join(value)
            else:
                value = '%s' % value

            value = value.replace(',', '|')
            value = value.replace('| ', '|')

            try:
                specification = Specification.objects.get(
                    domain=domain, attribute__key=key)
            except Specification.DoesNotExist:
                if autocreate_specification:
                    try:
                        attribute = Attribute.objects.get(key=key)
                    except Attribute.DoesNotExist:
                        attribute = Attribute.objects.create(
                            key=key, changeset=changeset)
                    specification = Specification.objects.create(
                        domain=domain, attribute=attribute, changeset=changeset)
                else:
                    continue

            try:
                obj = self.value_set.get(specification=specification)
            except Value.DoesNotExist:
                # in case there is no value for the specification, create
                obj = Value()
                obj.locality = self
                obj.specification = specification

            obj.data = value

            # check if Value.data actually changed, and save if it did
            if obj.tracker.changed():
                obj.changeset = changeset
                obj.save()
                changed_values.append(obj)
            else:
                # nothing changed, don't save the value
                pass

        # send values_updated signal
        signals.SIG_locality_values_updated.send(
            sender=self.__class__, instance=self
        )

        # calculate completeness
        if changed_values:
            self.completeness = self.calculate_completeness()
            self.save()

        return changed_values


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
    name = models.TextField()
    source = models.TextField(default='healthsites.io')


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


class DataLoader(models.Model):
    """
    """
    REPLACE_DATA_CODE = 1
    UPDATE_DATA_CODE = 2

    DATA_LOADER_MODE_CHOICES = (
        (REPLACE_DATA_CODE, 'Replace/Insert Data'),
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
        verbose_name='Organisation\'s Name',
        help_text='Organiation\'s Name',
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
        verbose_name='Data Loader Mode',
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
        verbose_name='Separator Character',
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

    def __unicode__(self):
        return u'%s' % (self.organisation_name)

    def save(self, *args, **kwargs):
        if not self.date_time_uploaded:
            self.date_time_uploaded = datetime.utcnow()
        super(DataLoader, self).save(*args, **kwargs)


# method for updating
def load_data(sender, instance, **kwargs):
    if not instance.applied:
        from .tasks import load_data_task
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


def validate_file_extension(value):
    if value.file.content_type != 'text/csv':
        raise ValidationError(u'Just receive csv file')


def get_trusted_user():
    from social_users.models import TrustedUser
    return TrustedUser.objects.values_list('user__id')


class DataLoaderPermission(models.Model):
    accepted_csv = models.FileField(
        verbose_name='Accepted CSV Data',
        help_text='Accepted CSV data that contains the data.',
        upload_to='accepted_csv_data/',
        max_length=100,
        validators=[validate_file_extension]
    )

    uploader = models.ForeignKey(
        User,
        verbose_name='Uploader',
        help_text='The user who propose the data loader.',
        null=False,
        limit_choices_to={
            'id__in': get_trusted_user,
        }
    )

    def __str__(self):
        return '%s : %s' % (self.accepted_csv, self.uploader)


def data_loader_deleted(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.accepted_csv.delete(False)


pre_delete.connect(data_loader_deleted, sender=DataLoaderPermission)


# -------------------------------------------------
# MASTERIZATION
# -------------------------------------------------


class UnconfirmedSynonym(models.Model):
    synonym = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='unconfirmed_synonym'
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='master_of_unconfirmed_synonym'
    )

    class Meta:
        ordering = ['locality', 'synonym']
        verbose_name = 'Potential Synonym'
        verbose_name_plural = 'Potential Synonyms'


class SynonymLocalities(models.Model):
    synonym = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='synonym_of_locality'
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='master_of_synonym'
    )

    class Meta:
        ordering = ['locality', 'synonym']
        verbose_name = 'Synonyms'
        verbose_name_plural = 'Synonyms'


def update_others_synonyms(sender, instance, **kwargs):
    from .masterization import downgrade_master_as_synonyms
    new_synonym = instance.synonym
    new_master = instance.locality
    downgrade_master_as_synonyms(new_synonym.id, new_master.id)


post_save.connect(update_others_synonyms, sender=SynonymLocalities)

# register signals
from . import signals  # noqa  # isort:skip
