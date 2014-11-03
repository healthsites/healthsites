# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import AttributeF, DomainSpecification1AF


class TestModelAttribute(TestCase):
    def test_model_repr(self):
        attr = AttributeF.create(key='An attribute')

        self.assertEqual(unicode(attr), 'an_attribute')

    def test_relations(self):
        attr1 = AttributeF.create(id=1, key='test')

        DomainSpecification1AF.create(
            name='A domain', attr1__attribute=attr1
        )

        self.assertEqual(
            [dom.name for dom in attr1.domain_set.all()],
            ['A domain']
        )

    def test_model_uniqueness(self):
        AttributeF.create(key='An attribute')

        self.assertRaises(
            IntegrityError, AttributeF.create, key='An attribute'
        )
