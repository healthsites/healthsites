# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import DomainF


class TestModelDomain(TestCase):
    def test_model_repr(self):
        domain = DomainF.create(name='A domain')

        self.assertEqual(unicode(domain), 'A domain')

    def test_model_uniqueness(self):
        DomainF.create(name='A domain')

        self.assertRaises(
            IntegrityError, DomainF.create, name='A domain'
        )
