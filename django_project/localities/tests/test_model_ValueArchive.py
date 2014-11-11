# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import ValueF, SpecificationF, LocalityF

from ..models import ValueArchive


class TestModelLocalityArchive(TestCase):
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
