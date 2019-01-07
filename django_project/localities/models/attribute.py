# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from django.utils.text import slugify

from model_utils import FieldTracker
from localities.models.mixin import ArchiveMixin, ChangesetMixin, UpdateMixin


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
