from django.test import TestCase

from .model_factories import LocalityF, LocalityValueF, AttributeF


class TestModelLocality(TestCase):
    def test_model_repr(self):
        locality = LocalityF.create(pk=1)

        self.assertEqual(unicode(locality), u'1')

    def test_model_with_value(self):
        attr = AttributeF.create(key='test')
        locality = LocalityValueF.create(
            pk=1, attr1__data='test', attr1__attribute=attr
        )

        self.assertEqual(unicode(locality), u'1')
        self.assertEqual(
            [unicode(val) for val in locality.value_set.all()],
            [u'(1) test=test']
        )
