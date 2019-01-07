# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models

from model_utils import FieldTracker
from localities.models.mixin import ArchiveMixin, ChangesetMixin, UpdateMixin


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
