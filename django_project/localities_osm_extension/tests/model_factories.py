# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

import factory
from ..models.extension import LocalityOSMExtension
from ..models.tag import Tag


class LocalityOSMExtensionF(factory.django.DjangoModelFactory):
    class Meta:
        model = LocalityOSMExtension


class TagF(factory.django.DjangoModelFactory):
    extension = factory.SubFactory(LocalityOSMExtensionF)
    name = factory.Sequence(lambda n: 'test_tag_{}'.format(n))
    value = factory.Sequence(lambda n: 'test_value_tag_{}'.format(n))

    class Meta:
        model = Tag
