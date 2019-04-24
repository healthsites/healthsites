# -*- coding: utf-8 -*-
import datetime
from unittest import skip

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from localities.tests.model_factories import (
    AttributeF, ChangesetF, DomainF, LocalityF, SpecificationF, ValueF
)
from social_users.tests.model_factories import UserF


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    @skip('skip')
    def test_localities_api_view(self):
        user = UserF.create(id=1, username='test')
        chgset = ChangesetF.create(
            social_user=user, created=datetime.datetime(2014, 11, 23, 12, 0)
        )
        dom = DomainF.create(name='test_domain', changeset=chgset)
        LocalityF.create(
            geom='POINT(16.9 45.4)', uuid='35570d8b22494bb6a88487a8108ffd69',
            changeset=chgset, domain=dom
        )

        LocalityF.create(
            geom='POINT(16 45)', uuid='35570d8b22494bb6a88487a8108ffd68',
            changeset=chgset, domain=dom
        )

        resp = self.client.get(
            reverse('api_localities'), {'bbox': '-180,-90,180,90'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'[{"version": 1, "user_id": 1, "uuid": "35570d8b22494bb6a88487a81'
            u'08ffd69", "lnglat": "16.9,45.4"}, {"version": 1, "user_id": 1, "'
            u'uuid": "35570d8b22494bb6a88487a8108ffd68", "lnglat": "16,45"}]'
        )

    @skip('skip')
    def test_localities_api_view_nodata(self):
        resp = self.client.get(
            reverse('api_localities'), {'bbox': '-180,-90,180,90'}
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content, u'[]')

    @skip('skip')
    def test_localities_api_view_missing_param(self):
        resp = self.client.get(reverse('api_localities'))

        self.assertEqual(resp.status_code, 404)

    @skip('skip')
    def test_localities_api_view_bad_bbox(self):
        resp = self.client.get(
            reverse('api_localities'), {'bbox': '-b,-a,b,a'}
        )

        self.assertEqual(resp.status_code, 404)

    @skip('skip')
    def test_locality_api_view(self):
        user = UserF.create(id=1, username='test')
        chgset = ChangesetF.create(
            id=1, social_user=user,
            created=datetime.datetime(2014, 11, 23, 12, 0)
        )
        dom = DomainF.create(name='test_domain', changeset=chgset)

        attr = AttributeF.create(key='test', changeset=chgset)

        spec = SpecificationF.create(
            domain=dom, attribute=attr, changeset=chgset
        )

        loc = LocalityF.create(
            geom='POINT(16.9 45.4)', uuid='35570d8b22494bb6a88487a8108ffd69',
            changeset=chgset, domain=dom
        )

        ValueF.create(
            changeset=chgset, specification=spec, locality=loc,
            data='test val'
        )

        resp = self.client.get(
            reverse(
                'api_locality',
                kwargs={'uuid': '35570d8b22494bb6a88487a8108ffd69'}
            )
        )

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'{"geom": [16.9, 45.4], "version": 1, "values": {"test": "test va'
            u'l"}, "uuid": "35570d8b22494bb6a88487a8108ffd69", "changeset": 1}'
        )

    @skip('skip')
    def test_locality_api_view_nodata(self):
        resp = self.client.get(
            reverse(
                'api_locality',
                kwargs={'uuid': '35570d8b22494bb6a88487a8108ffd69'}
            )
        )

        self.assertEqual(resp.status_code, 404)
