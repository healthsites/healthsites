from django.test import TestCase

from .model_factories import GroupF


class TestModelGroup(TestCase):
    def test_model_repr(self):
        group = GroupF.create(name='A group')

        self.assertEqual(unicode(group), 'A group')
