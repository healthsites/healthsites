# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

import random
from django.test import TestCase
from .model_factories import TagF, LocalityOSMExtensionF


class TestTagModel(TestCase):

    def test_tag_create(self):
        """Test Tag model creation."""

        model = TagF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)


class TestLocalityOSMExtension(TestCase):

    def test_locality_osm_extension_create(self):
        """Test locality healthsites osm model creation."""

        tag1 = TagF.create()
        tag2 = TagF.create()

        self.assertTrue(tag1.pk is not None)
        self.assertTrue(tag2.pk is not None)

        model = LocalityOSMExtensionF.create(
            osm_id=random.randint(1, 99999),
            osm_pk=random.randint(1, 99),
            osm_type='node',
            custom_tag=(tag1, tag2)
        )

        self.assertTrue(model.pk is not None)
        self.assertTrue(len(model.custom_tag.all()) is 2)
