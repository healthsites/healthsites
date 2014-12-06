# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import DomainF

from ..models import Domain


class TestModelDomain(TestCase):
    def test_Domain_fields(self):
        self.assertListEqual(
            [fld.name for fld in Domain._meta.fields], [
                u'id', 'changeset', 'version', 'name', 'description',
                'template_fragment'
            ]
        )

    def test_model_repr(self):
        domain = DomainF.create(name='A domain')

        self.assertEqual(str(domain), 'A domain')

    def test_model_uniqueness(self):
        DomainF.create(name='A domain')

        self.assertRaises(
            IntegrityError, DomainF.create, name='A domain'
        )
