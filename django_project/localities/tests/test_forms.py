# -*- coding: utf-8 -*-
from django.test import TestCase

from .model_factories import LocalityValueF, GroupF, AttributeF, LocalityF

from ..forms import LocalityForm


class TestImporters(TestCase):
    def test_dynamicformfields(self):
        grp = GroupF.create(name='test')
        AttributeF.create(key='test', in_groups=[grp])
        AttributeF.create(key='osm', in_groups=[grp])

        loc = LocalityF.create(geom='POINT(16 45)', group=grp)

        frm = LocalityForm(loc)

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
        grp = GroupF()
        test_attr = AttributeF.create(key='test', in_groups=[grp])

        loc = LocalityValueF.create(
            id=1, geom='POINT(16 45)', uuid='93b7e8c4621a4597938dfd3d27659162',
            attr1__attribute=test_attr, attr1__data='osm', group=grp
        )

        frm = LocalityForm(loc)

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
