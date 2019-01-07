# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.conf import settings
from django.contrib.gis.db import models
from django.utils import timezone


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
