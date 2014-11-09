# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType


from .models import Domain, DomainArchive


@receiver(post_save, sender=Domain)
def domain_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='domain')
    archive = DomainArchive()
    archive.content_type = ct
    archive.object_id = instance.pk

    archive.version = instance.version
    archive.changeset = instance.changeset

    archive.name = instance.name
    archive.description = instance.description
    archive.template_fragment = instance.template_fragment

    archive.save()
