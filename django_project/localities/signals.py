# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType

from .models import (
    Domain,
    DomainArchive,
    Attribute,
    AttributeArchive,
    Specification,
    SpecificationArchive,
    Locality,
    LocalityArchive,
    LocalityIndex,
    Value,
    ValueArchive
)

# define custom signals
SIG_locality_values_updated = Signal()


def archive_basic_info(archive, instance, content_type):
    """
    Helper function that handles archival of basic object information, like
    *content_type*, *object_id*, *version* and *changeset*
    """

    archive.content_type = content_type
    archive.object_id = instance.pk

    archive.version = instance.version
    archive.changeset = instance.changeset


@receiver(post_save, sender=Domain)
def domain_archive_handler(sender, instance, created, raw, **kwargs):
    """
    *post_save* triggered change archival for a Domain object
    """

    ct = ContentType.objects.get(app_label='localities', model='domain')
    archive = DomainArchive()

    archive_basic_info(archive, instance, ct)

    archive.name = instance.name
    archive.description = instance.description
    archive.template_fragment = instance.template_fragment

    archive.save()


@receiver(post_save, sender=Attribute)
def attribute_archive_handler(sender, instance, created, raw, **kwargs):
    """
    *post_save* triggered change archival for an Attribute object
    """

    ct = ContentType.objects.get(app_label='localities', model='attribute')
    archive = AttributeArchive()

    archive_basic_info(archive, instance, ct)

    archive.key = instance.key
    archive.description = instance.description

    archive.save()


@receiver(post_save, sender=Specification)
def specification_archive_handler(sender, instance, created, raw, **kwargs):
    """
    *post_save* triggered change archival for a Specification object
    """

    ct = ContentType.objects.get(app_label='localities', model='specification')
    archive = SpecificationArchive()

    archive_basic_info(archive, instance, ct)

    archive.domain_id = instance.domain.pk
    archive.attribute_id = instance.attribute.pk
    archive.required = instance.required

    archive.save()


@receiver(post_save, sender=Locality)
def locality_archive_handler(sender, instance, created, raw, **kwargs):
    """
    *post_save* triggered change archival for a Locality object
    """

    ct = ContentType.objects.get(app_label='localities', model='locality')
    archive = LocalityArchive()

    archive_basic_info(archive, instance, ct)

    archive.domain_id = instance.domain.pk
    archive.uuid = instance.uuid
    archive.upstream_id = instance.upstream_id
    archive.geom = instance.geom
    archive.master = instance.master

    if instance.master:
        synonyms = instance.get_synonyms()
        for synonym in synonyms:
            if synonym == instance.master:
                synonym.master = None
            else:
                synonym.master = instance.master
            synonym.save()
    archive.save()


@receiver(post_save, sender=Value)
def value_archive_handler(sender, instance, created, raw, **kwargs):
    """
    *post_save* triggered change archival for a Value object
    """

    ct = ContentType.objects.get(app_label='localities', model='value')
    archive = ValueArchive()

    archive_basic_info(archive, instance, ct)

    archive.locality_id = instance.locality.pk
    archive.specification_id = instance.specification.pk
    archive.data = instance.data

    archive.save()


@receiver(SIG_locality_values_updated, sender=Locality)
def values_updated_handler(sender, instance, **kwargs):
    """
    *SIG_locality_values_updated* triggered LocalityIndex update for a Locality
    """

    LOG.debug('Updating LocalityIndex for Locality: %s', instance.pk)

    # retrieve ranked attribute values for a Locality
    loc_fts = instance.prepare_for_fts()

    # in case there is no index for the Locality, create one
    locind = LocalityIndex.objects.get_or_create(locality=instance)[0]

    # either we got some data or set to ''
    locind.ranka = loc_fts.get('A', '')
    locind.rankb = loc_fts.get('B', '')
    locind.rankc = loc_fts.get('C', '')
    locind.rankd = loc_fts.get('D', '')

    locind.save()
