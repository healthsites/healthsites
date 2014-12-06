# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import (
    AttributeF,
    LocalityF,
    DomainSpecification2AF,
    DomainSpecification3AF
)

from ..importers import CSVImporter
from ..models import Locality, Value
from ..exceptions import LocalityImportError


class TestImporters(TestCase):
    def test_ok_data(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='url')
        attr3 = AttributeF.create(key='services')

        DomainSpecification3AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2,
            spec3__attribute=attr3
        )

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.csv',
            './localities/tests/test_data/test_csv_import_map.json'
        )

        self.assertEqual(Locality.objects.count(), 3)
        self.assertEqual(Value.objects.count(), 8)

    def test_ok_data_tabs(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='url')
        attr3 = AttributeF.create(key='services')

        DomainSpecification3AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2,
            spec3__attribute=attr3
        )

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.tsv',
            './localities/tests/test_data/test_csv_import_map.json',
            use_tabs=True
        )

        self.assertEqual(Locality.objects.count(), 3)
        self.assertEqual(Value.objects.count(), 8)

    def test_ok_data_bad_domain(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='url')
        attr3 = AttributeF.create(key='services')

        DomainSpecification3AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2,
            spec3__attribute=attr3
        )

        self.assertRaises(
            LocalityImportError, CSVImporter,
            'Test-error', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.csv',
            './localities/tests/test_data/test_csv_import_map.json'
        )

    def test_missing_upstream_id(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='url')
        attr3 = AttributeF.create(key='services')

        DomainSpecification3AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2,
            spec3__attribute=attr3
        )

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv',
            './localities/tests/test_data/test_csv_import_map.json'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 6)

    def test_find_by_upstream_id(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='services')

        dom = DomainSpecification2AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2
        )

        loc = LocalityF.create(upstream_id='test_imp¶2', domain=dom)

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv',
            './localities/tests/test_data/test_csv_import_map.json'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 4)

        self.assertListEqual(
            list(loc.value_set.values_list('data', flat=True)), [
                u'HIV Treatment; HIV Counseling; HIV Testing',
                u'Athalia Satellite Clinic'
            ])

    def test_find_by_uuid(self):
        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='services')

        dom = DomainSpecification2AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2
        )

        loc = LocalityF.create(
            uuid='93b7e8c4621a4597938dfd3d27659162', domain=dom
        )

        CSVImporter(
            'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_bad.csv',
            './localities/tests/test_data/test_csv_import_map.json'
        )

        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Value.objects.count(), 4)

        self.assertListEqual(
            list(loc.value_set.values_list('data', flat=True)), [
                u'HIV Treatment; HIV Counseling; HIV Testing',
                u'Andrieskraal Satellite Clinic'
            ])
