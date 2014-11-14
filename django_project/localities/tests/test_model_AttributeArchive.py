# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import AttributeF

from ..models import AttributeArchive


class TestModelAttributeArchive(TestCase):

    def test_attributeArchive_fields(self):
        self.assertListEqual(
            [fld.name for fld in AttributeArchive._meta.fields], [
                u'id', 'changeset', 'version', 'content_type', 'object_id',
                'key', 'description'
            ]
        )

    def test_archiving_attribute(self):
        attribute = AttributeF.create(key='A key')

        attribute.description = 'a new descritpion'
        attribute.save()

        attribute.key = 'a new key'
        attribute.save()

        attribute.key = 'A key'
        attribute.save()

        # test save with no changes, should not trigger model archival
        attribute.key = 'A key'
        attribute.save()

        self.assertEqual(AttributeArchive.objects.count(), 4)

        self.assertListEqual(
            [attr.key for attr in AttributeArchive.objects.all()],
            ['a_key', 'a_key', 'a_new_key', 'a_key']
        )

        self.assertListEqual(
            [attr.version for attr in AttributeArchive.objects.all()],
            [1, 2, 3, 4]
        )
