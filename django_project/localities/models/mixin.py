# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.gis.db import models


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
