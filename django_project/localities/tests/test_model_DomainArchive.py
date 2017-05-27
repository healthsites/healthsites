# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import DomainArchive
from .model_factories import DomainF


class TestModelDomainArchive(TestCase):
    def test_domainArchive_fields(self):
        self.assertListEqual(
            [fld.name for fld in DomainArchive._meta.fields], [
                u'id', 'changeset', 'version', 'content_type', 'object_id',
                'name', 'description', 'template_fragment'
            ]
        )

    def test_archiving(self):
        domain = DomainF.create(name='A domain')

        domain.name = 'test'
        domain.save()

        domain.description = 'a description'
        domain.save()

        # test save with no changes, should not trigger model archival
        domain.save()

        self.assertEqual(DomainArchive.objects.count(), 3)

        self.assertListEqual(
            [dom.name for dom in DomainArchive.objects.all()],
            ['A domain', 'test', 'test']
        )

        self.assertListEqual(
            [dom.version for dom in DomainArchive.objects.all()],
            [1, 2, 3]
        )
