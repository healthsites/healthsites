# -*- coding: utf-8 -*-
import datetime
from unittest import skip

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from social_users.tests.model_factories import UserF

from ..models import Locality
from .model_factories import (
    AttributeF, ChangesetF, DomainSpecification1AF,
    DomainSpecification2AF, LocalityF, LocalityValue1F, LocalityValue2F
)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    @skip('skip')
    def test_localities_view(self):
        LocalityF.create(
            uuid='93b7e8c4621a4597938dfd3d27659162', geom='POINT(16 45)'
        )
        resp = self.client.get(reverse('localities'), data={
            'zoom': 1,
            'bbox': '-180,-90,180,90',
            'iconsize': '40,40',
            'geoname': '',
            'tag': '',
            'spec': '',
            'data': '',
            'uuid': ''
        })

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(
            resp.content, (
                u'[{"count": 1, "minbbox": [16.0, 45.0, 16.0, 45.0], "geom": ['
                u'16.0, 45.0], "uuid": "93b7e8c4621a4597938dfd3d27659162", "bb'
                u'ox": [-13.831067331307473, 15.168932668692527, 45.8310673313'
                u'0747, 74.83106733130748]}]'
            )
        )

    def test_localities_view_bad_params(self):
        resp = self.client.get(reverse('localities'), data={
            'bbox': '-180,-90,180,90'
        })

        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('localities'), data={
            'zoom': 'a',
            'bbox': 'b,c,d,e',
            'iconsize': 'f,g'
        })

        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('localities'), data={
            'zoom': '21',
            'bbox': '-180,-90,180,90',
            'iconsize': '34,34'
        })

        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(reverse('localities'), data={
            'zoom': '1',
            'bbox': '-180,-90,180,90',
            'iconsize': '-34,34'
        })

        self.assertEqual(resp.status_code, 404)

    def test_localitiesInfo_view(self):
        chgset = ChangesetF.create(id=1, created=datetime.datetime(2017, 5, 12, 12, 0, 0))

        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(
            template_fragment='Test value: {{ values.test }}',
            spec1__attribute=test_attr
        )
        LocalityValue1F.create(
            geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification__attribute=test_attr, val1__data='osm',
            domain=dom, changeset=chgset
        )

        resp = self.client.get(reverse(
            'locality-info', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }
        ))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(len(resp.content), 480)

    @skip('skip')
    def test_localitiesUpdate_form_get_no_user(self):
        resp = self.client.get(reverse(
            'locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }
        ))

        self.assertEqual(resp.status_code, 403)

    @skip('skip')
    def test_localitiesUpdate_form_get(self):
        UserF(username='test', password='test')

        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        LocalityValue1F.create(
            geom='POINT(16 45)', val1__data='osm', domain=dom,
            uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification__attribute=test_attr
        )

        self.client.login(username='test', password='test')
        resp = self.client.get(reverse(
            'locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }
        ))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'text/html; charset=utf-8')

        self.assertContains(
            resp,
            '<input id="id_lon" name="lon" step="any" type="number" value="16.'
            '0" />',
            html=True
        )
        self.assertContains(
            resp,
            '<input id="id_lat" name="lat" step="any" type="number" value="45.'
            '0" />',
            html=True
        )
        self.assertContains(
            resp,
            '<input class="form-control" id="id_test" name="test" type="text" '
            'value="osm" />',
            html=True
        )

    @skip('skip')
    def test_localitiesUpdate_form_post(self):
        UserF(username='test', password='test')
        test_attr = AttributeF.create(key='test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            geom='POINT(16 45)', val1__data='osm', domain=dom,
            uuid='93b7e8c4621a4597938dfd3d27659162', val1__specification=spec,
            changeset=chgset, val1__changeset=chgset
        )
        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        self.client.login(username='test', password='test')
        resp = self.client.post(
            reverse('locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }
            ), {'test': 'new_osm', 'lon': 10, 'lat': 35}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(uuid='93b7e8c4621a4597938dfd3d27659162')

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
        ]))

    @skip('skip')
    def test_localitiesUpdate_form_post_no_data_update(self):
        UserF(username='test', password='test')

        test_attr = AttributeF.create(key='test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            geom='POINT(16 45)', val1__data='test_osm', domain=dom,
            uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification=spec, changeset=chgset, val1__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        self.client.login(username='test', password='test')
        resp = self.client.post(
            reverse('locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }), {'test': 'test_osm', 'lon': 16, 'lat': 45}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(uuid='93b7e8c4621a4597938dfd3d27659162')

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

    @skip('skip')
    def test_localitiesUpdate_form_post_partial_data_update_locality(self):
        UserF(username='test', password='test')

        test_attr = AttributeF.create(key='test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        spec = dom.specification_set.all()[0]

        org_loc = LocalityValue1F.create(
            geom='POINT(16 45)', val1__data='test_osm', domain=dom,
            uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification=spec, changeset=chgset, val1__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        self.client.login(username='test', password='test')
        resp = self.client.post(reverse(
            'locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }), {'test': 'test_osm', 'lon': 16, 'lat': 10}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(uuid='93b7e8c4621a4597938dfd3d27659162')

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

    @skip('skip')
    def test_localitiesUpdate_form_post_partial_data_update_values(self):
        UserF(username='test', password='test')
        test_attr = AttributeF.create(key='test')
        test_attr2 = AttributeF.create(key='other_test')
        chgset = ChangesetF.create(id=1)

        dom = DomainSpecification2AF(
            spec1__attribute=test_attr, spec2__attribute=test_attr2
        )

        spec = [spec for spec in dom.specification_set.all()]

        org_loc = LocalityValue2F.create(
            geom='POINT(16 45)', domain=dom, changeset=chgset,
            uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__data='test_osm', val1__specification=spec[0],
            val1__changeset=chgset, val2__data='other_osm',
            val2__specification=spec[1], val2__changeset=chgset
        )

        org_loc_version = org_loc.version
        org_value_versions = [
            org_val.version for org_val in org_loc.value_set.all()
        ]

        self.client.login(username='test', password='test')
        resp = self.client.post(reverse(
            'locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }), {
            'test': 'new_test_osm', 'other_test': 'other_osm', 'lon': 16,
            'lat': 45
        })

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, 'OK')

        loc = Locality.objects.get(uuid='93b7e8c4621a4597938dfd3d27659162')

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
            [True, False]
        )

    @skip('skip')
    def test_localitiesUpdate_form_post_fail(self):
        UserF(username='test', password='test')
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF(spec1__attribute=test_attr)

        LocalityValue1F.create(
            geom='POINT(16 45)', val1__data='osm', domain=dom,
            uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification__attribute=test_attr
        )

        self.client.login(username='test', password='test')
        resp = self.client.post(reverse(
            'locality-update', kwargs={
                'uuid': '93b7e8c4621a4597938dfd3d27659162'
            }
        ), {'test': 'new_osm'})

        self.assertEqual(resp.status_code, 200)

        self.assertFormError(resp, 'form', 'lat', [u'This field is required.'])
        self.assertFormError(resp, 'form', 'lon', [u'This field is required.'])

    @skip('skip')
    def test_localitiesCreate_form_get_no_user(self):
        resp = self.client.get(
            reverse('locality-create', kwargs={'domain': 'test'})
        )
        self.assertEqual(resp.status_code, 403)

    @skip('skip')
    def test_localitiesCreate_form_get(self):
        UserF(username='test', password='test')
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

        self.client.login(username='test', password='test')
        resp = self.client.get(
            reverse('locality-create', kwargs={'domain': 'test'})
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp['Content-Type'], 'text/html; charset=utf-8')

        self.assertContains(
            resp,
            '<input id="id_lon" name="lon" step="any" type="number" />',
            html=True
        )
        self.assertContains(
            resp,
            '<input id="id_lat" name="lat" step="any" type="number" />',
            html=True
        )
        self.assertContains(
            resp,
            '<input id="id_test" name="test" type="text" />',
            html=True
        )

    @skip('skip')
    def test_localitiesCreate_form_post(self):
        UserF(username='test', password='test')
        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

        self.client.login(username='test', password='test')
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
        self.assertEqual(loc.version, 1)

    @skip('skip')
    def test_localitiesCreate_form_post_fail(self):
        UserF(username='test', password='test')

        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(name='test', spec1__attribute=test_attr)

        self.client.login(username='test', password='test')
        resp = self.client.post(
            reverse('locality-create', kwargs={'domain': 'test'}),
            {'test': 'new_osm'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertFormError(resp, 'form', 'lat', [u'This field is required.'])
        self.assertFormError(resp, 'form', 'lon', [u'This field is required.'])

    @skip('skip')
    def test_localitiesCreate_form_post_required_attr(self):
        UserF(username='test', password='test')

        test_attr = AttributeF.create(key='test')
        DomainSpecification1AF(
            name='test', spec1__attribute=test_attr, spec1__required=True
        )

        self.client.login(username='test', password='test')
        resp = self.client.post(
            reverse('locality-create', kwargs={'domain': 'test'}),
            {'test': ''}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertFormError(resp, 'form', 'lat', [u'This field is required.'])
        self.assertFormError(resp, 'form', 'lon', [u'This field is required.'])
