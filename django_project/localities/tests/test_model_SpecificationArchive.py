# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import SpecificationF, DomainF, AttributeF

from ..models import SpecificationArchive


class TestModelSpecificationArchive(TestCase):
    def test_archiving_specification(self):
        attribute = AttributeF(id=1, key='A key')
        domain = DomainF(id=1, name='A domain')
        specification = SpecificationF.create(
            attribute=attribute, domain=domain
        )

        specification.required = True
        specification.save()

        attribute2 = AttributeF(id=2, key='A new key')
        specification.attribute = attribute2
        specification.save()

        # test save with no changes, should not trigger model archival
        specification.required = True
        specification.save()

        self.assertEqual(SpecificationArchive.objects.count(), 3)

        self.assertListEqual(
            [spec.attribute_id for spec in SpecificationArchive.objects.all()],
            [1, 1, 2]
        )

        self.assertListEqual(
            [spec.version for spec in SpecificationArchive.objects.all()],
            [1, 2, 3]
        )
