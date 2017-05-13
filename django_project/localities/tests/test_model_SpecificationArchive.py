# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import SpecificationArchive
from .model_factories import AttributeF, DomainF, SpecificationF


class TestModelSpecificationArchive(TestCase):
    def test_specificationArchive_fields(self):
        self.assertListEqual(
            [fld.name for fld in SpecificationArchive._meta.fields], [
                u'id', 'changeset', 'version', 'content_type', 'object_id',
                'domain_id', 'attribute_id', 'required', 'fts_rank'
            ]
        )

    def test_archiving_specification(self):
        attribute = AttributeF(id=1, key='A key')
        domain = DomainF(id=1, name='A domain')
        specification = SpecificationF.create(
            attribute=attribute, domain=domain, fts_rank='A'
        )

        specification.required = True
        specification.fts_rank = 'B'
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
