from django.test import TestCase

from .model_factories import ValueF, LocalityF, AttributeF


class TestModelValue(TestCase):
    def test_model_repr(self):
        loc = LocalityF.create(id=1)
        attr = AttributeF.create(name='An attribute')
        value = ValueF.create(locality=loc, attribute=attr, data='test')

        self.assertEqual(unicode(value), '(1) An attribute=test')
