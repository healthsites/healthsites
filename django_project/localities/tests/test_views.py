# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from localities.tests.model_factories import (
    LocalityF,
    LocalityValueF,
    AttributeF,
    GroupF
)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_localities_view(self):
        LocalityF.create(id=1, geom='POINT(16 45)')
        resp = self.client.get(reverse('localities'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(resp.content, '[{"i": 1, "g": [16.0, 45.0]}]')

    def test_localitiesInfo_view(self):
        grp = GroupF(template_fragment='Test value: {{ values.test }}')
        test_attr = AttributeF.create(key='test', in_groups=[grp])

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            attr1__attribute=test_attr, attr1__data='osm', group=grp
        )

        resp = self.client.get(reverse('locality-info', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(
            resp.content, (
                '{"geom": [16.0, 45.0], "values": {"test": "osm"}, "id": 1, '
                '"repr": "Test value: osm", "uuid": "93b7e8c4621a4597938dfd3d'
                '27659162"}'
            )
        )
