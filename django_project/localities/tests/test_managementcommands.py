# -*- coding: utf-8 -*-
from unittest import skip

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from ..models import Locality, Value
from .model_factories import AttributeF, DomainSpecification3AF


class TestManagementCommands(TestCase):
    @skip('skip')
    def test_import_csv(self):

        attr1 = AttributeF.create(key='name')
        attr2 = AttributeF.create(key='url')
        attr3 = AttributeF.create(key='services')

        DomainSpecification3AF.create(
            name='Test', spec1__attribute=attr1, spec2__attribute=attr2,
            spec3__attribute=attr3
        )

        call_command(
            'import_csv', 'Test', 'test_imp',
            './localities/tests/test_data/test_csv_import_ok.tsv',
            './localities/tests/test_data/test_csv_import_map.json',
            use_tabs=True
        )

        self.assertEqual(Locality.objects.count(), 3)
        self.assertEqual(Value.objects.count(), 8)

    def test_import_csv_bad_arguments(self):

        self.assertRaises(
            CommandError, call_command, 'import_csv', 'Test', 'test_imp'
        )
