from django.test import TestCase

from .model_factories import AttributeF, GroupF


class TestModelAttribute(TestCase):
    def test_model_repr(self):
        attr = AttributeF.create(name='An attribute')

        self.assertEqual(unicode(attr), 'An attribute')

    def test_relations(self):
        group = GroupF.create(name='A group')
        attr = AttributeF.create(name='An attribute', in_group=[group])

        self.assertEqual(
            [group.name for group in attr.in_group.all()],
            ['A group']
        )
