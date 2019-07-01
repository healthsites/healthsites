__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from localities_osm_extension.models.extension import LocalityOSMExtension


class PendingState(models.Model):
    """ Model for telling pending create/update."""

    extension = models.OneToOneField(
        LocalityOSMExtension)

    uploader = models.ForeignKey(User)
    time_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=512)
    version = models.IntegerField()
