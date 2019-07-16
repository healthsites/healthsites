__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from localities_osm_extension.models.extension import LocalityOSMExtension


class PendingUpdate(models.Model):
    """ Model for telling pending create/update."""

    extension = models.OneToOneField(
        LocalityOSMExtension)

    uploader = models.ForeignKey(User)
    time_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=512)
    version = models.IntegerField()


class PendingReview(models.Model):
    """Model for telling pending review caused by possibly data duplication."""

    uploader = models.ForeignKey(User)
    name = models.CharField(max_length=512)
    reason = models.TextField(null=True, blank=True, default='')
    payload = models.TextField(null=True, blank=True, default='')
    time_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
