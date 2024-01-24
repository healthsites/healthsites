__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from .extension import LocalityOSMExtension  # noqa


class PendingUpdate(models.Model):
    """
    This model is about update that already pushed
    but still not pulled into docker osm cache.
    """

    extension = models.OneToOneField(
        LocalityOSMExtension, on_delete=models.CASCADE)

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    time_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=512)
    version = models.IntegerField()


class PendingReview(models.Model):
    """
     This model is about update that failed to be saved.
     """

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    reason = models.TextField(null=True, blank=True, default='')
    payload = models.TextField(null=True, blank=True, default='')
    time_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
