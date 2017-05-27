# -*- coding: utf-8 -*-
from django.test import TestCase

from ..forms import DomainForm, DomainModelForm, LocalityForm
from .model_factories import (
    AttributeF, DomainSpecification1AF, DomainSpecification2AF, LocalityF, LocalityValue1F
)


class TestLocalityForms(TestCase):
    def test_LocalityForm(self):
        attr1 = AttributeF.create(key='test')
        attr2 = AttributeF.create(key='osm')

        dom = DomainSpecification2AF.create(
            name='test', spec1__attribute=attr1, spec2__attribute=attr2
        )

        loc = LocalityF.create(geom='POINT(16 45)', domain=dom)

        frm = LocalityForm(locality=loc)
        self.assertEqual(len(frm.fields), 4)

    def test_LocalityForm_initialdata(self):
        test_attr = AttributeF.create(key='test')

        dom = DomainSpecification1AF.create(
            spec1__attribute=test_attr
        )

        loc = LocalityValue1F.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            val1__specification__attribute=test_attr, val1__data='osm',
            domain=dom
        )

        frm = LocalityForm(locality=loc)

        self.assertEqual(frm['test'].value(), u'osm')
        self.assertEqual(frm['lat'].value(), 45.0)
        self.assertEqual(frm['lon'].value(), 16.0)

    def test_DomainForm(self):
        attr1 = AttributeF.create(key='test')
        attr2 = AttributeF.create(key='osm')

        dom = DomainSpecification2AF.create(
            name='test', spec1__attribute=attr1, spec2__attribute=attr2
        )

        frm = DomainForm(domain=dom)

        self.assertEqual(
            frm.as_ul(), (
                u'<li><label for="id_lon">Lon:</label> <input id="id_lon" name'
                u'="lon" step="any" type="number" /></li>\n<li><label for="id_'
                u'lat">Lat:</label> <input id="id_lat" name="lat" step="any" t'
                u'ype="number" /></li>\n<li><label for="id_test">test:</label>'
                u' <input id="id_test" name="test" type="text" /></li>\n<li><l'
                u'abel for="id_osm">osm:</label> <input id="id_osm" name="osm"'
                u' type="text" /></li>'
            )
        )

    def test_DomainModelForm_bad_fragment(self):
        frm = DomainModelForm(
            {'name': 'Test', 'template_fragment': '{% bad_template %}'}
        )
        self.assertFalse(frm.is_valid())
        self.assertDictEqual(
            frm.errors, {
                'template_fragment': [
                    u"Template Syntax Error: Invalid block tag: 'bad_template'"
                ]
            }
        )

    def test_DomainModelForm_ok_data(self):
        frm = DomainModelForm(
            {'name': 'Test', 'template_fragment': '{{ test }}'}
        )
        self.assertTrue(frm.is_valid())
