# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

import factory
from ..models.extension import LocalityOSMExtension
from ..models.tag import Tag


class TagF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'test_tag_{}'.format(n))
    value = factory.Sequence(lambda n: 'test_value_tag_{}'.format(n))

    class Meta:
        model = Tag


class LocalityOSMExtensionF(factory.django.DjangoModelFactory):
    class Meta:
        model = LocalityOSMExtension

    @factory.post_generation
    def custom_tag(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.custom_tag.add(tag)
