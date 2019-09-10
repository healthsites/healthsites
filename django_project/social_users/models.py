# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.db.models.signals import pre_delete

from localities.models import DataLoaderPermission

LOG = logging.getLogger(__name__)


class Profile(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
        User, default=1)
    profile_picture = models.CharField(
        default='', max_length=512, blank=True)
    osm_name = models.CharField(
        default='', max_length=512, blank=True)


class GatherUser(models.Model):
    """
    This is gather user information
    """

    user = models.OneToOneField(
        User, default=1)
    gather_id = models.IntegerField()
    gather_password = models.CharField(max_length=512)

    def __unicode__(self):
        return u'%s' % self.user


class Organisation(models.Model):
    """
    Extention of User
    """

    name = models.CharField(blank=False, max_length=64)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, default=None)
    contact = models.CharField(default='', blank=True, max_length=64)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    trusted_users = models.ManyToManyField(
        'TrustedUser', through='OrganisationSupported', blank=True
    )

    def clean_website(self):
        if 'http' in self.site.domain:
            return self.site.domain
        else:
            return 'http://' + self.site.domain

    def __unicode__(self):
        name = u'%s' % self.name
        if self.site:
            name += ' (%s)' % self.clean_website()
        return name


class TrustedUser(models.Model):
    """
    Extention of User
    """

    user = models.OneToOneField(
        User, default=1, unique=True)
    organisations_supported = models.ManyToManyField(
        'Organisation', through=Organisation.trusted_users.through, blank=True
    )


class OrganisationSupported(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(TrustedUser, on_delete=models.CASCADE)
    is_staff = models.BooleanField(
        verbose_name='Is Staff',
        default=False
    )
    date_added = models.DateField(default=datetime.now)


def trusted_user_deleted(sender, instance, **kwargs):
    DataLoaderPermission.objects.filter(uploader=instance.user).delete()


pre_delete.connect(trusted_user_deleted, sender=TrustedUser)
