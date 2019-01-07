# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete


class DataLoader(models.Model):
    """
    """
    REPLACE_DATA_CODE = 1
    UPDATE_DATA_CODE = 2

    DATA_LOADER_MODE_CHOICES = (
        (REPLACE_DATA_CODE, 'Replace/Insert Data'),
        (UPDATE_DATA_CODE, 'Update Data')
    )

    COMMA_CHAR = ','
    TAB_CHAR = '\t'

    COMMA_CODE = 1  # ,
    TAB_CODE = 2  # \t

    SEPARATORS = {
        COMMA_CODE: COMMA_CHAR,
        TAB_CODE: TAB_CHAR
    }

    SEPARATOR_CHOICES = (
        (COMMA_CODE, 'Comma'),
        (TAB_CODE, 'Tab'),
    )

    organisation_name = models.CharField(
        verbose_name='Organisation\'s Name',
        help_text='Organiation\'s Name',
        null=False,
        blank=False,
        max_length=100
    )

    json_concept_mapping = models.FileField(
        verbose_name='JSON Concept Mapping',
        help_text='JSON Concept Mapping File.',
        upload_to='json_mapping/%Y/%m/%d',
        max_length=100
    )

    csv_data = models.FileField(
        verbose_name='CSV Data',
        help_text='CSV data that contains the data.',
        upload_to='csv_data/%Y/%m/%d',
        max_length=100
    )

    data_loader_mode = models.IntegerField(
        choices=DATA_LOADER_MODE_CHOICES,
        verbose_name='Data Loader Mode',
        help_text='The mode of the data loader.',
        blank=False,
        null=False
    )

    applied = models.BooleanField(
        verbose_name='Applied',
        help_text='Whether the data update has been applied or not.',
        default=False
    )

    author = models.ForeignKey(
        User,
        verbose_name='Author',
        help_text='The user who propose the data loader.',
        null=False
    )

    date_time_uploaded = models.DateTimeField(
        verbose_name='Uploaded (time)',
        help_text='Timestamp (UTC) when the data uploaded',
        null=False,
    )

    date_time_applied = models.DateTimeField(
        verbose_name='Applied (time)',
        help_text='When the data applied (loaded)',
        null=True
    )

    separator = models.IntegerField(
        choices=SEPARATOR_CHOICES,
        verbose_name='Separator Character',
        help_text='Separator character.',
        null=False,
        default=COMMA_CODE
    )

    notes = models.TextField(
        verbose_name='Notes',
        help_text='Notes',
        null=True,
        blank=True,
        default=''
    )

    def __str__(self):
        return self.organisation_name

    def __unicode__(self):
        return u'%s' % (self.organisation_name)

    def save(self, *args, **kwargs):
        if not self.date_time_uploaded:
            self.date_time_uploaded = datetime.utcnow()
        super(DataLoader, self).save(*args, **kwargs)


# method for updating
def load_data(sender, instance, **kwargs):
    if not instance.applied:
        from localities.tasks import load_data_task
        load_data_task.delay(instance.pk)


# register the signal
post_save.connect(load_data, sender=DataLoader)


# ---------------------------------
# DATA LOADER PERMISSION
# ---------------------------------
def validate_file_extension(value):
    if value.file.content_type != 'text/csv':
        raise ValidationError(u'Just receive csv file')


def get_trusted_user():
    from social_users.models import TrustedUser
    return TrustedUser.objects.values_list('user__id')


class DataLoaderPermission(models.Model):
    accepted_csv = models.FileField(
        verbose_name='Accepted CSV Data',
        help_text='Accepted CSV data that contains the data.',
        upload_to='accepted_csv_data/',
        max_length=100,
        validators=[validate_file_extension]
    )

    uploader = models.ForeignKey(
        User,
        verbose_name='Uploader',
        help_text='The user who propose the data loader.',
        null=False,
        limit_choices_to={
            'id__in': get_trusted_user,
        }
    )

    def __str__(self):
        return '%s : %s' % (self.accepted_csv, self.uploader)


def data_loader_deleted(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.accepted_csv.delete(False)


pre_delete.connect(data_loader_deleted, sender=DataLoaderPermission)
