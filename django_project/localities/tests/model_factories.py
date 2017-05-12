# -*- coding: utf-8 -*-
import factory

from ..models import Attribute, Changeset, Domain, Locality, Specification, Value


class DomainF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "domain_{}".format(n))
    description = ''
    template_fragment = ''
    changeset = factory.SubFactory(
        'localities.tests.model_factories.ChangesetF'
    )
    version = None  # set to None, helps test version increment robustness

    class Meta:
        model = Domain


class AttributeF(factory.django.DjangoModelFactory):
    key = factory.Sequence(lambda n: "attribute_{}".format(n))
    description = ''
    changeset = factory.SubFactory(
        'localities.tests.model_factories.ChangesetF'
    )
    version = None  # set to None, helps test version increment robustness

    class Meta:
        model = Attribute


class LocalityF(factory.django.DjangoModelFactory):
    domain = factory.SubFactory('localities.tests.model_factories.DomainF')
    uuid = factory.Sequence(lambda n: "uuid_{}".format(n))
    upstream_id = factory.Sequence(lambda n: "upstream_id_{}".format(n))
    geom = 'POINT (0 0)'
    changeset = factory.SubFactory(
        'localities.tests.model_factories.ChangesetF'
    )
    version = None  # set to None, helps test version increment robustness

    class Meta:
        model = Locality


class LocalityValue1F(LocalityF):
    val1 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )


class LocalityValue2F(LocalityF):
    val1 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )
    val2 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )


class LocalityValue4F(LocalityF):
    val1 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )
    val2 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )
    val3 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )
    val4 = factory.RelatedFactory(
        'localities.tests.model_factories.ValueF', 'locality'
    )


class ValueF(factory.django.DjangoModelFactory):
    locality = factory.SubFactory('localities.tests.model_factories.LocalityF')
    specification = factory.SubFactory(
        'localities.tests.model_factories.SpecificationF',
    )
    data = ''
    changeset = factory.SubFactory(
        'localities.tests.model_factories.ChangesetF'
    )
    version = None  # set to None, helps test version increment robustness

    class Meta:
        model = Value


class SpecificationF(factory.django.DjangoModelFactory):
    domain = factory.SubFactory('localities.tests.model_factories.DomainF')
    attribute = factory.SubFactory(
        'localities.tests.model_factories.AttributeF',
    )
    required = False
    fts_rank = 'D'
    changeset = factory.SubFactory(
        'localities.tests.model_factories.ChangesetF'
    )
    version = None  # set to None, helps test version increment robustness

    class Meta:
        model = Specification


class DomainSpecification1AF(DomainF):
    spec1 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )


class DomainSpecification2AF(DomainF):
    spec1 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec2 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )


class DomainSpecification3AF(DomainF):
    spec1 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec2 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec3 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )


class DomainSpecification4AF(DomainF):
    spec1 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec2 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec3 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )
    spec4 = factory.RelatedFactory(
        'localities.tests.model_factories.SpecificationF', 'domain'
    )


class ChangesetF(factory.django.DjangoModelFactory):
    social_user = factory.SubFactory(
        'social_users.tests.model_factories.UserF'
    )
    created = None
    comment = ''

    class Meta:
        model = Changeset
