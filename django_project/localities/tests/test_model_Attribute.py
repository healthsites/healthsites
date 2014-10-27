# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import AttributeF, GroupF


class TestModelAttribute(TestCase):
    def test_model_repr(self):
        attr = AttributeF.create(key='An attribute')

        self.assertEqual(unicode(attr), 'an_attribute')

    def test_relations(self):
        group = GroupF.create(name='A group')
        attr = AttributeF.create(key='An attribute', in_groups=[group])

        self.assertEqual(
            [group.name for group in attr.in_groups.all()],
            ['A group']
        )

    def test_model_uniqueness(self):
        AttributeF.create(key='An attribute')

        self.assertRaises(
            IntegrityError, AttributeF.create, key='An attribute'
        )
