# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.flatpages.models import FlatPage


class CustomFlatPage(FlatPage):
    """Model to extend django flatpage."""

    enrollment_title = models.CharField(
        max_length=200,
        unique=True
    )
    gather_url = models.CharField(max_length=250)
    gather_username = models.CharField(max_length=250)
    gather_password = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.title = self.enrollment_title
        self.url = '/{}/'.format(self.title.replace(' ', '-'))
        super(CustomFlatPage, self).save(*args, **kwargs)
