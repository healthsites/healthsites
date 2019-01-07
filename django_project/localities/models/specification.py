# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models

from model_utils import FieldTracker
from localities.models.mixin import ArchiveMixin, ChangesetMixin, UpdateMixin

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
