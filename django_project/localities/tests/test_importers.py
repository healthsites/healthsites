# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import AttributeF, GroupF, LocalityF

from ..importers import CSVImporter
from ..models import Locality, Value
from ..exceptions import LocalityImportError


class TestImporters(TestCase):
    def test_ok_data(self):
        group = GroupF.create(name='Test')
        AttributeF.create(key='name', in_groups=[group])
        AttributeF.create(key='url', in_groups=[group])
        AttributeF.create(key='services', in_groups=[group])

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.csv'
        )

        self.assertEqual(Locality.objects.count(), 3)
        self.assertEqual(Value.objects.count(), 9)

    def test_ok_data_bad_group(self):
        group = GroupF.create(name='Test')
        AttributeF.create(key='name', in_groups=[group])
        AttributeF.create(key='url', in_groups=[group])
        AttributeF.create(key='services', in_groups=[group])

        self.assertRaises(
            LocalityImportError, CSVImporter,
            'Test-error', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.csv'
        )

    def test_missing_upstream_id(self):
        group = GroupF.create(name='Test')
        AttributeF.create(key='name', in_groups=[group])
        AttributeF.create(key='url', in_groups=[group])
        AttributeF.create(key='services', in_groups=[group])

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 6)

    def test_find_by_upstream_id(self):
        group = GroupF.create(name='Test')
        AttributeF.create(key='name', in_groups=[group])
        AttributeF.create(key='services', in_groups=[group])

        loc = LocalityF.create(upstream_id='test_imp¶2')

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 4)

        self.assertEqual(
            list(loc.value_set.values_list('data', flat=True)), [
                u'HIV Treatment; HIV Counseling; HIV Testing',
                u'Athalia Satellite Clinic'
            ])

    def test_find_by_uuid(self):
        group = GroupF.create(name='Test')
        AttributeF.create(key='name', in_groups=[group])
        AttributeF.create(key='services', in_groups=[group])

        loc = LocalityF.create(uuid='93b7e8c4621a4597938dfd3d27659162')

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 4)

        self.assertEqual(
            list(loc.value_set.values_list('data', flat=True)), [
                u'HIV Treatment; HIV Counseling; HIV Testing',
                u'Andrieskraal Satellite Clinic'
            ])
