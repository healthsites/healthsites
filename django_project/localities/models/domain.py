# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from model_utils import FieldTracker
from localities.models.mixin import ArchiveMixin, ChangesetMixin, UpdateMixin


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
