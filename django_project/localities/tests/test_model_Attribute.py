# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import AttributeF, DomainSpecification1AF

from ..models import Attribute


class TestModelAttribute(TestCase):

    def test_Attribute_fields(self):
        self.assertListEqual(
            [fld.name for fld in Attribute._meta.fields], [
                u'id', 'changeset', 'version', 'key', 'description'
            ]
        )

    def test_model_repr(self):
        attr = AttributeF.create(key='An attribute')

        self.assertEqual(str(attr), 'an_attribute')

    def test_relations(self):
        attr1 = AttributeF.create(id=1, key='test')

        DomainSpecification1AF.create(
            name='A domain', spec1__attribute=attr1
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
