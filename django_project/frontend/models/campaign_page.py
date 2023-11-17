# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.flatpages.models import FlatPage
from social_users.models import Organisation


class CampaignPage(FlatPage):
    """Model to extend django flatpage."""
    campaign_title = models.CharField(
        max_length=200,
        unique=True
    )
    gather_url = models.CharField(
        max_length=250)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.title = self.campaign_title
        self.url = '/{}/'.format(self.title.replace(' ', '-'))
        super(CampaignPage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Campaign Page'
        verbose_name_plural = 'Campaign Pages'
