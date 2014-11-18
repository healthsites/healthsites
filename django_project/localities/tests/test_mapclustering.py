# -*- coding: utf-8 -*-
from django.test import TestCase


from .model_factories import LocalityF

from ..map_clustering import within_bbox, cluster, overlapping_area

from ..models import Locality


class TestMapClustering(TestCase):
    def test_within_bbox(self):

        bbox = (0, 0, 180, 90)

        self.assertTrue(within_bbox(bbox, 10, 10))
        self.assertFalse(within_bbox(bbox, -10, 10))
        self.assertFalse(within_bbox(bbox, 10, 99))

    def test_overlapping_area(self):

        self.assertEqual(
            overlapping_area(zoom=0, pix_x=10, pix_y=10, lat=0),
            (14.0625, 14.0625)
        )

        self.assertEqual(
            overlapping_area(zoom=3, pix_x=10, pix_y=10, lat=45),
            (1.2429611388044781, 1.2429611388044781)
        )

        self.assertEqual(
            overlapping_area(zoom=6, pix_x=10, pix_y=10, lat=60),
            (0.10986328125000001, 0.10986328125000001)
        )

    def test_cluster(self):

        LocalityF.create(id=1)
        LocalityF.create(id=2)
        LocalityF.create(id=3)
        LocalityF.create(id=4)
        LocalityF.create(id=5)

        LocalityF.create(id=6, geom='POINT(30 30)')
        LocalityF.create(id=7, geom='POINT(32 32)')

        LocalityF.create(id=8, geom='POINT(45 45)')

        queryset = Locality.objects.all()

        dict_cluster = cluster(queryset, 3, 40, 40)

        self.assertListEqual(dict_cluster, [
            {'count': 5, 'geom': (0.0, 0.0), 'id': 1,
                'bbox': (-10.546875, -10.546875, 10.546875, 10.546875)},
            {'count': 2, 'geom': (30.0, 30.0), 'id': 6,
                'bbox': (
                    20.866138319460998, 20.866138319460998,
                    39.133861680539, 39.133861680539)},
            {'count': 1, 'geom': (45.0, 45.0), 'id': 8,
                'bbox': (
                    37.54223316717313, 37.54223316717313,
                    52.45776683282687, 52.45776683282687)}
            ])
