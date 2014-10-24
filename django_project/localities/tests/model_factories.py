import factory

from ..models import (
    Group,
    Locality,
    Value,
    Attribute
)


class GroupF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "group_{}".format(n))
    description = ''

    class Meta:
        model = Group


class AttributeF(factory.django.DjangoModelFactory):
    key = factory.Sequence(lambda n: "attribute_{}".format(n))
    description = ''

    @factory.post_generation
    def in_groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.in_groups.add(group)

    class Meta:
        model = Attribute


class LocalityF(factory.django.DjangoModelFactory):
    group = factory.SubFactory('localities.tests.model_factories.GroupF')
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
