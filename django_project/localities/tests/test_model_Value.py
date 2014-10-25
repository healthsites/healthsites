from django.test import TestCase

from django.db import IntegrityError

from .model_factories import ValueF, LocalityF, AttributeF


class TestModelValue(TestCase):
    def test_model_repr(self):
        loc = LocalityF.create(id=1)
        attr = AttributeF.create(key='An attribute')
        value = ValueF.create(locality=loc, attribute=attr, data='test')

        self.assertEqual(unicode(value), '(1) an-attribute=test')

    def test_model_uniqueness(self):
        loc = LocalityF.create()
        attr = AttributeF.create()
        ValueF.create(locality=loc, attribute=attr)

        self.assertRaises(
            IntegrityError, ValueF.create, locality=loc, attribute=attr
        )
