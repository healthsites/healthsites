# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .model_factories import (
    LocalityF,
    LocalityValueF,
    AttributeF,
    DomainSpecification1AF
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
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(
            template_fragment='Test value: {{ values.test }}',
            attr1__attribute=test_attr
        )
        LocalityValueF.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            attr1__attribute=test_attr, attr1__data='osm', domain=dom
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
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(
            attr1__attribute=test_attr
        )

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', domain=dom
        )

        resp = self.client.get(reverse('locality-update', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'text/html; charset=utf-8')

        self.assertEqual(
            resp.content,
            u'<form>\n<p><label for="id_lon">Lon:</label> <input id="id_lon" n'
            u'ame="lon" step="any" type="number" value="16.0" /></p>\n<p><labe'
            u'l for="id_lat">Lat:</label> <input id="id_lat" name="lat" step="'
            u'any" type="number" value="45.0" /></p>\n<p><label for="id_test">'
            u'test:</label> <input id="id_test" name="test" type="text" value='
            u'"osm" /></p>\n</form>'
        )

    def test_localitiesUpdate_form_post(self):
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(
            attr1__attribute=test_attr
        )

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', domain=dom
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
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(
            attr1__attribute=test_attr
        )

        LocalityValueF.create(
            id=1, geom='POINT(16 45)', attr1__attribute=test_attr,
            attr1__data='osm', domain=dom
        )

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}),
            {'test': 'new_osm'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'<form>\n<ul class="errorlist"><li>This field is required.</li></'
            u'ul>\n<p><label for="id_lon">Lon:</label> <input id="id_lon" name'
            u'="lon" step="any" type="number" /></p>\n<ul class="errorlist"><l'
            u'i>This field is required.</li></ul>\n<p><label for="id_lat">Lat:'
            u'</label> <input id="id_lat" name="lat" step="any" type="number" '
            u'/></p>\n<p><label for="id_test">test:</label> <input id="id_test'
            u'" name="test" type="text" value="new_osm" /></p>\n</form>'
        )

    def test_localitiesCreate_form_get(self):
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(
            name='test', attr1__attribute=test_attr
        )

        resp = self.client.get(
            reverse('locality-create', kwargs={'domain': 'test'})
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'text/html; charset=utf-8')

        self.assertEqual(
            resp.content,
            u'<form>\n<p><label for="id_lon">Lon:</label> <input id="id_lon" n'
            u'ame="lon" step="any" type="number" /></p>\n<p><label for="id_lat'
            u'">Lat:</label> <input id="id_lat" name="lat" step="any" type="nu'
            u'mber" /></p>\n<p><label for="id_test">test:</label> <input id="i'
            u'd_test" name="test" type="text" /></p>\n</form>'
        )

    def test_localitiesCreate_form_post(self):
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(
            name='test', attr1__attribute=test_attr
        )

        resp = self.client.post(
            reverse('locality-create', kwargs={'domain': 'test'}),
            {'test': 'new_osm', 'lon': 10, 'lat': 35}
        )

        self.assertEqual(resp.status_code, 200)

        # check if got back an id, can be parsed as int
        self.assertTrue(int(resp.content) != 0)

        loc = Locality.objects.get()

        self.assertEqual(loc.geom.x, 10.0)
        self.assertEqual(loc.geom.y, 35.0)

        self.assertListEqual(
            [val.data for val in loc.value_set.all()],
            ['new_osm']
        )

    def test_localitiesCreate_form_post_fail(self):
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(
            name='test', attr1__attribute=test_attr
        )

        resp = self.client.post(
            reverse('locality-create', kwargs={'domain': 'test'}),
            {'test': 'new_osm'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'<form>\n<ul class="errorlist"><li>This field is required.</li></'
            u'ul>\n<p><label for="id_lon">Lon:</label> <input id="id_lon" name'
            u'="lon" step="any" type="number" /></p>\n<ul class="errorlist"><l'
            u'i>This field is required.</li></ul>\n<p><label for="id_lat">Lat:'
            u'</label> <input id="id_lat" name="lat" step="any" type="number" '
            u'/></p>\n<p><label for="id_test">test:</label> <input id="id_test'
            u'" name="test" type="text" value="new_osm" /></p>\n</form>'
        )
