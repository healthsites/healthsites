# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .model_factories import (
    LocalityF,
    LocalityValue1F,
    LocalityValue2F,
    AttributeF,
    DomainSpecification1AF,
    DomainSpecification2AF,
    ChangesetF
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
            spec1__attribute=test_attr
        )
        LocalityValue1F.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification__attribute=test_attr, val1__data='osm',
            domain=dom
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

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        LocalityValue1F.create(
            id=1, geom='POINT(16 45)', val1__data='osm', domain=dom,
            val1__specification__attribute=test_attr
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
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            id=1, geom='POINT(16 45)', val1__data='osm', domain=dom,
            val1__specification=spec, changeset=chgset, val1__changeset=chgset
        )
        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

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

        # check if we got a new changeset
        self.assertNotEqual(loc.changeset.id, chgset.id)

        self.assertTrue(all(
            True for val in loc.value_set.all()
            if val.changeset == loc.changeset
        ))
        self.assertFalse(any(
            True for val in loc.value_set.all()
            if val.changeset == chgset.id
        ))

        # test version, should be increased by 1
        self.assertEqual(loc.version, org_loc_version + 1)

        # test values version, should CHANGE
        self.assertFalse(any([
            True for idx, val in enumerate(loc.value_set.all())
            if val.version == org_value_versions[idx]
            ])
        )

    def test_localitiesUpdate_form_post_no_data_update(self):
        test_attr = AttributeF.create(key='test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            id=1, geom='POINT(16 45)', val1__data='test_osm', domain=dom,
            val1__specification=spec, changeset=chgset, val1__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}),
            {'test': 'test_osm', 'lon': 16, 'lat': 45}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(pk=1)

        self.assertEqual(loc.geom.x, 16.0)
        self.assertEqual(loc.geom.y, 45.0)

        self.assertListEqual(
            [val.data for val in loc.value_set.all()],
            ['test_osm']
        )

        # check if we got the SAME changeset (as data did NOT CHANGE)
        self.assertEqual(loc.changeset.id, chgset.id)

        # value changeset should NOT CHANGE
        self.assertTrue(all(
            True for val in loc.value_set.all()
            if val.changeset.id == chgset.id
        ))

        # test version, should NOT CHANGE
        self.assertEqual(loc.version, org_loc_version)

        # test values version, should NOT CHANGE
        self.assertListEqual(
            [val.version for val in loc.value_set.all()],
            org_value_versions
        )

    def test_localitiesUpdate_form_post_partial_data_update_locality(self):
        test_attr = AttributeF.create(key='test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            id=1, geom='POINT(16 45)', val1__data='test_osm', domain=dom,
            val1__specification=spec, changeset=chgset, val1__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}),
            {'test': 'test_osm', 'lon': 16, 'lat': 10}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(pk=1)

        self.assertEqual(loc.geom.x, 16.0)
        self.assertEqual(loc.geom.y, 10.0)

        self.assertListEqual(
            [val.data for val in loc.value_set.all()],
            ['test_osm']
        )

        # check if we got a new changeset (data CHANGE)
        self.assertNotEqual(loc.changeset.id, chgset.id)

        # value changeset should NOT change
        self.assertTrue(all(
            True for val in loc.value_set.all()
            if val.changeset.id == chgset.id
        ))

        # test version, should CHANGE
        self.assertNotEqual(loc.version, org_loc_version)

        # test values version, should NOT CHANGE
        self.assertListEqual(
            [val.version for val in loc.value_set.all()],
            org_value_versions
        )

    def test_localitiesUpdate_form_post_partial_data_update_values(self):
        test_attr = AttributeF.create(key='test')
        test_attr2 = AttributeF.create(key='other_test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification2AF(
            spec1__attribute=test_attr, spec2__attribute=test_attr2
        )

        spec = [spec for spec in dom.specification_set.all()]

        org_loc = LocalityValue2F.create(
            id=1, geom='POINT(16 45)', domain=dom, changeset=chgset,
            val1__data='test_osm', val1__specification=spec[0],
            val1__changeset=chgset, val2__data='other_osm',
            val2__specification=spec[1], val2__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        resp = self.client.post(
            reverse('locality-update', kwargs={'pk': 1}), {
                'test': 'new_test_osm', 'other_test': 'other_osm', 'lon': 16,
                'lat': 45
            }
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(pk=1)

        self.assertEqual(loc.geom.x, 16.0)
        self.assertEqual(loc.geom.y, 45.0)

        self.assertListEqual(
            [val.data for val in loc.value_set.all()],
            [u'other_osm', u'new_test_osm']
        )

        # check if we got the SAME changeset (NO data CHANGE)
        self.assertEqual(loc.changeset.id, chgset.id)

        # value changeset of one attribute should CHANGE
        self.assertListEqual(
            [val.changeset.id == chgset.id for val in loc.value_set.all()],
            [True, False]
        )

        # test version, should NOT CHANGE
        self.assertEqual(loc.version, org_loc_version)

        # test values version, should CHANGE
        self.assertListEqual(
            [val.version == org_value_versions[idx]
                for idx, val in enumerate(loc.value_set.all())],
            [False, True]
        )

    def test_localitiesUpdate_form_post_fail(self):
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        LocalityValue1F.create(
            id=1, geom='POINT(16 45)', val1__data='osm', domain=dom,
            val1__specification__attribute=test_attr
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
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

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
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

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

        # test version
        self.assertTrue(loc.version == 1)

    def test_localitiesCreate_form_post_fail(self):
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

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

    def test_localitiesCreate_form_post_required_attr(self):
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(
            name='test', spec1__attribute=test_attr, spec1__required=True
        )

        resp = self.client.post(
            reverse('locality-create', kwargs={'domain': 'test'}),
            {'test': ''}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'<form>\n<ul class="errorlist"><li>This field is required.</li></'
            u'ul>\n<p><label for="id_lon">Lon:</label> <input id="id_lon" name'
            u'="lon" step="any" type="number" /></p>\n<ul class="errorlist"><l'
            u'i>This field is required.</li></ul>\n<p><label for="id_lat">Lat:'
            u'</label> <input id="id_lat" name="lat" step="any" type="number" '
            u'/></p>\n<ul class="errorlist"><li>This field is required.</li></'
            u'ul>\n<p><label for="id_test">test:</label> <input id="id_test" n'
            u'ame="test" type="text" /></p>\n</form>'
        )
