# -*- coding: utf-8 -*-
import factory

from ..models import (
    Domain,
    Locality,
    Value,
    Attribute
)


class DomainF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "domain_{}".format(n))
    description = ''
    template_fragment = ''

    class Meta:
        model = Domain


class AttributeF(factory.django.DjangoModelFactory):
    key = factory.Sequence(lambda n: "attribute_{}".format(n))
    description = ''

    @factory.post_generation
    def in_domains(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for domain in extracted:
                self.in_domains.add(domain)

    class Meta:
        model = Attribute


class LocalityF(factory.django.DjangoModelFactory):
    domain = factory.SubFactory('localities.tests.model_factories.DomainF')
    uuid = factory.Sequence(lambda n: "uuid_{}".format(n))
    upstream_id = factory.Sequence(lambda n: "upstream_id_{}".format(n))
    geom = 'POINT (0 0)'
    created = None
    modified = None

    class Meta:
        model = Locality


class LocalityValueF(LocalityF):
    attr1 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )


class ValueF(factory.django.DjangoModelFactory):
    locality = factory.SubFactory('localities.tests.model_factories.LocalityF')
    attribute = factory.SubFactory(
        'localities.tests.model_factories.AttributeF',
    )
    data = ''

    class Meta:
        model = Value
