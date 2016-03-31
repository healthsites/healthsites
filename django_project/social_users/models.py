# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import itertools
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import pre_delete


class Profile(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
        User, default=1)
    profile_picture = models.CharField(default="", max_length=150, blank=True)
    screen_name = models.CharField(default="", max_length=50, blank=True)


class Organization(models.Model):
    """
    Extention of User
    """

    name = models.CharField(blank=False, max_length=64)
    website = models.CharField(default="", blank=True, max_length=64)
    contact = models.CharField(default="", blank=True, max_length=64)
    trusted_users = models.ManyToManyField('TrustedUser', through='Membership', blank=True)

    def clean_website(self):
        if "http" in self.website:
            return self.website
        else :
            return "http://"+self.website

    def __unicode__(self):
        return u'%s' % (self.name)


class TrustedUser(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
        User, default=1, unique=True)
    organizations = models.ManyToManyField('Organization', through=Organization.trusted_users.through, blank=True)


class Membership(models.Model):
    organisation = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(TrustedUser, on_delete=models.CASCADE)
    date_added = models.DateField()
    invite_reason = models.CharField(max_length=64, blank=True)


def trusted_user_deleted(sender, instance, **kwargs):
    DataLoaderPermission.objects.filter(uploader=instance.user).delete()


from localities.models import DataLoaderPermission
pre_delete.connect(trusted_user_deleted, sender=TrustedUser)
