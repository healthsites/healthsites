# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import (
    LocalityValue1F,
    AttributeF,
    LocalityF,
    DomainSpecification2AF,
    DomainSpecification1AF
)

from ..forms import LocalityForm, DomainForm


class TestLocalityForms(TestCase):
    def test_LocalityForm(self):
        attr1 = AttributeF.create(key='test')
        attr2 = AttributeF.create(key='osm')

        dom = DomainSpecification2AF.create(
            name='test', spec1__attribute=attr1, spec2__attribute=attr2
        )

        loc = LocalityF.create(geom='POINT(16 45)', domain=dom)

        frm = LocalityForm(locality=loc)

        self.assertEqual(
            frm.as_ul(), (
                u'<li><label for="id_lon">Lon:</label> <input id="id_lon" name'
                u'="lon" step="any" type="number" value="16.0" /></li>\n<li><l'
                u'abel for="id_lat">Lat:</label> <input id="id_lat" name="lat"'
                u' step="any" type="number" value="45.0" /></li>\n<li><label f'
                u'or="id_test">test:</label> <input id="id_test" name="test" t'
                u'ype="text" /></li>\n<li><label for="id_osm">osm:</label> <in'
                u'put id="id_osm" name="osm" type="text" /></li>'
            )
        )

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

        self.assertEqual(
            frm.as_ul(), (
                u'<li><label for="id_lon">Lon:</label> <input id="id_lon" name'
                u'="lon" step="any" type="number" value="16.0" /></li>\n<li><l'
                u'abel for="id_lat">Lat:</label> <input id="id_lat" name="lat"'
                u' step="any" type="number" value="45.0" /></li>\n<li><label f'
                u'or="id_test">test:</label> <input id="id_test" name="test" t'
                u'ype="text" value="osm" /></li>'
            )
        )

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
