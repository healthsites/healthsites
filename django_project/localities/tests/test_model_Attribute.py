# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import AttributeF, DomainF


class TestModelAttribute(TestCase):
    def test_model_repr(self):
        attr = AttributeF.create(key='An attribute')

        self.assertEqual(unicode(attr), 'an_attribute')

    def test_relations(self):
        domain = DomainF.create(name='A domain')
        attr = AttributeF.create(key='An attribute', in_domains=[domain])

        self.assertEqual(
            [dom.name for dom in attr.in_domains.all()],
            ['A domain']
        )

    def test_model_uniqueness(self):
        AttributeF.create(key='An attribute')

        self.assertRaises(
            IntegrityError, AttributeF.create, key='An attribute'
        )
