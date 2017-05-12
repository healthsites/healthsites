# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import ValueArchive
from .model_factories import LocalityF, SpecificationF, ValueF


class TestModelLocalityArchive(TestCase):
    def test_valueArchive_fields(self):
        self.assertListEqual(
            [fld.name for fld in ValueArchive._meta.fields], [
                u'id', 'changeset', 'version', 'content_type', 'object_id',
                'locality_id', 'specification_id', 'data'
            ]
        )

    def test_archiving_locality(self):
        specification = SpecificationF.create()
        locality = LocalityF.create()
        value = ValueF.create(
            specification=specification, locality=locality, data='test'
        )

        value.data = 'new data'
        value.save()

        # test save with no changes, should not trigger model archival
        value.save()

        self.assertEqual(ValueArchive.objects.count(), 2)

        self.assertListEqual(
            [val.data for val in ValueArchive.objects.all()],
            ['test', 'new data']
        )

        self.assertListEqual(
            [val.version for val in ValueArchive.objects.all()],
            [1, 2]
        )
