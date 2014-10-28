# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .model_factories import (
    LocalityF,
    LocalityValueF,
    AttributeF,
    GroupF
)

from ..models import Locality


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

    def test_localitiesUpdate_form_get(self):
        grp = GroupF()
        test_attr = AttributeF.create(key='test', in_groups=[grp])

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', group=grp
        )

        resp = self.client.get(reverse('locality-update', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'text/html; charset=utf-8')

        self.assertEqual(
            resp.content,
            u'<tr><th><label for="id_lon">Lon:</label></th><td><input id="id_l'
            u'on" name="lon" step="any" type="number" value="16.0" /></td></tr'
            u'>\n<tr><th><label for="id_lat">Lat:</label></th><td><input id="i'
            u'd_lat" name="lat" step="any" type="number" value="45.0" /></td><'
            u'/tr>\n<tr><th><label for="id_test">test:</label></th><td><input '
            u'id="id_test" name="test" type="text" value="osm" /></td></tr>'
        )

    def test_localitiesUpdate_form_post(self):
        grp = GroupF()
        test_attr = AttributeF.create(key='test', in_groups=[grp])

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', group=grp
        )

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}),
            {'test': 'new_osm', 'lon': 10, 'lat': 35}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(pk=1)

        self.assertEqual(loc.geom.x, 10.0)
        self.assertEqual(loc.geom.y, 35.0)

        self.assertListEqual(
            [val.data for val in loc.value_set.all()],
            ['new_osm']
        )

    def test_localitiesUpdate_form_post_fail(self):
        grp = GroupF()
        test_attr = AttributeF.create(key='test', in_groups=[grp])

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', group=grp
        )

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}),
            {'test': 'new_osm'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'<tr><th><label for="id_lon">Lon:</label></th><td><ul class="erro'
            u'rlist"><li>This field is required.</li></ul><input id="id_lon" n'
            u'ame="lon" step="any" type="number" /></td></tr>\n<tr><th><label '
            u'for="id_lat">Lat:</label></th><td><ul class="errorlist"><li>This'
            u' field is required.</li></ul><input id="id_lat" name="lat" step='
            u'"any" type="number" /></td></tr>\n<tr><th><label for="id_test">t'
            u'est:</label></th><td><input id="id_test" name="test" type="text"'
            u' value="new_osm" /></td></tr>'
        )
