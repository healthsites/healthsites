# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from localities.tests.model_factories import (
    LocalityF,
    AttributeF,
    SpecificationF,
    ValueF,
    DomainF,
    ChangesetF
)

from social_users.tests.model_factories import UserF


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

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

        resp = self.client.get(reverse('api_localities'))

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(
            resp.content,
            u'[{"version": 1, "user_id": 1, "uuid": "35570d8b22494bb6a88487a81'
            u'08ffd69", "lnglat": "16.9,45.4"}, {"version": 1, "user_id": 1, "'
            u'uuid": "35570d8b22494bb6a88487a8108ffd68", "lnglat": "16,45"}]'
        )
