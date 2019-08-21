# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '24/02/19'

import random
from django.test import TestCase
from .model_factories import TagF, LocalityOSMExtensionF


class TestLocalityOSMExtension(TestCase):

    def test_locality_osm_extension_create(self):
        """Test locality healthsites osm model creation."""

        model = LocalityOSMExtensionF.create(
            osm_id=random.randint(1, 99999),
            osm_type='node'
        )

        self.assertTrue(model.pk is not None)


class TestTagModel(TestCase):

    def test_tag_create(self):
        """Test Tag model creation."""

        extension = LocalityOSMExtensionF.create()
        model = TagF.create(
            extension=extension
        )

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)
