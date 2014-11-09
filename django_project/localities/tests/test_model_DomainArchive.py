# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import DomainF

from ..models import DomainArchive


class TestModelDomainArchive(TestCase):
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
