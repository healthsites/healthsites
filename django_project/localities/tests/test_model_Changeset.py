# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import ChangesetF


class TestModelChangeset(TestCase):
    def test_model_repr(self):
        chgset = ChangesetF.create(pk=1)

        self.assertEqual(unicode(chgset), '1')
        self.assertTrue(chgset.created is not None)

    def test_model_update(self):
        chgset = ChangesetF.create(pk=1)

        created = chgset.created

        # update changeset
        chgset.comment = 'a new comment'
        chgset.save()

        self.assertEqual(chgset.created, created)
