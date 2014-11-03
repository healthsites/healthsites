# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import (
    ValueF,
    LocalityF,
    AttributeF,
    SpecificationF
)


class TestModelValue(TestCase):
    def test_model_repr(self):
        loc = LocalityF.create(id=1)
        attr = AttributeF.create(key='An attribute')
        value = ValueF.create(
            locality=loc, specification__attribute=attr, data='test'
        )

        self.assertEqual(unicode(value), '(1) an_attribute=test')

    def test_model_uniqueness(self):
        loc = LocalityF.create()
        spec = SpecificationF.create()
        ValueF.create(locality=loc, specification=spec)

        self.assertRaises(
            IntegrityError, ValueF.create,
            locality=loc, specification=spec
        )
