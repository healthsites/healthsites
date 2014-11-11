# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.gis.geos import Point

from .model_factories import LocalityF, DomainF

from ..models import LocalityArchive


class TestModelLocalityArchive(TestCase):
    def test_archiving_locality(self):
        domain = DomainF(id=1, name='A domain')
        locality = LocalityF.create(domain=domain)

        locality.geom = Point(1, 1)
        locality.save()

        # test save with no changes, should not trigger model archival
        locality.save()

        self.assertEqual(LocalityArchive.objects.count(), 2)

        self.assertListEqual(
            [loc.geom.ewkt for loc in LocalityArchive.objects.all()], [
                u'SRID=4326;POINT (0.0000000000000000 0.0000000000000000)',
                u'SRID=4326;POINT (1.0000000000000000 1.0000000000000000)'
            ]
        )

        self.assertListEqual(
            [loc.version for loc in LocalityArchive.objects.all()],
            [1, 2]
        )
