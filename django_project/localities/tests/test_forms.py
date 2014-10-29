# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import LocalityValueF, DomainF, AttributeF, LocalityF

from ..forms import LocalityForm


class TestImporters(TestCase):
    def test_dynamicformfields(self):
        dom = DomainF.create(name='test')
        AttributeF.create(key='test', in_domains=[dom])
        AttributeF.create(key='osm', in_domains=[dom])

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

    def test_dynamicform_initialdata(self):
        dom = DomainF()
        test_attr = AttributeF.create(key='test', in_domains=[dom])

        loc = LocalityValueF.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            attr1__attribute=test_attr, attr1__data='osm', domain=dom
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
