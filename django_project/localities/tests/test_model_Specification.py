# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import (
    SpecificationF,
    DomainF,
    AttributeF
)


class TestModelSpecification(TestCase):
    def test_model_repr(self):
        dom = DomainF.create(id=1, name='A domain')
        attr = AttributeF.create(key='An attribute')
        spec = SpecificationF.create(domain=dom, attribute=attr)

        self.assertEqual(unicode(spec), 'A domain an_attribute')

    def test_model_uniqueness(self):
        dom = DomainF.create(id=1)
        attr = AttributeF.create(id=1, key='An attribute')
        SpecificationF.create(domain=dom, attribute=attr)

        self.assertRaises(
            IntegrityError, SpecificationF.create,
            domain=dom, attribute=attr
        )
