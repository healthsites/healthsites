# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from localities.models.locality import Locality


class UnconfirmedSynonym(models.Model):
    synonym = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='unconfirmed_synonym'
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='master_of_unconfirmed_synonym'
    )

    class Meta:
        ordering = ['locality', 'synonym']
        verbose_name = 'Potential Synonym'
        verbose_name_plural = 'Potential Synonyms'


class SynonymLocalities(models.Model):
    synonym = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='synonym_of_locality'
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='master_of_synonym'
    )

    class Meta:
        ordering = ['locality', 'synonym']
        verbose_name = 'Synonyms'
        verbose_name_plural = 'Synonyms'


def update_others_synonyms(sender, instance, **kwargs):
    from localities.masterization import downgrade_master_as_synonyms
    new_synonym = instance.synonym
    new_master = instance.locality
    downgrade_master_as_synonyms(new_synonym.id, new_master.id)


post_save.connect(update_others_synonyms, sender=SynonymLocalities)
