# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from .model_factories import LocalityF, LocalityValueF, AttributeF, GroupF


class TestModelLocality(TestCase):
    def test_model_repr(self):
        locality = LocalityF.create(pk=1)

        self.assertEqual(unicode(locality), u'1')

    def test_model_with_value(self):
        attr = AttributeF.create(key='test')
        locality = LocalityValueF.create(
            pk=1, attr1__data='test', attr1__attribute=attr
        )

        self.assertEqual(unicode(locality), u'1')
        self.assertEqual(
            [unicode(val) for val in locality.value_set.all()],
            [u'(1) test=test']
        )

    def test_get_attr_map(self):
        gr = GroupF.create(name='a group')

        AttributeF.create(id=1, key='test', in_groups=[gr])
        AttributeF.create(id=2, key='osm', in_groups=[gr])

        # this group should not be in results
        gr2 = GroupF.create(name='a group')
        AttributeF.create(key='osm2', in_groups=[gr2])

        locality = LocalityF.create(group=gr)

        self.assertEqual(
            list(locality.get_attr_map()),
            [{'id': 1, 'key': u'test'}, {'id': 2, 'key': u'osm'}]
        )

    def test_set_values(self):
        gr = GroupF.create(name='a group')

        AttributeF.create(key='test', in_groups=[gr])
        AttributeF.create(key='osm', in_groups=[gr])

        locality = LocalityF.create(pk=1, group=gr)

        value_map = {'osm': 'osm val', 'test': 'test val'}
        chg_values = locality.set_values(value_map)

        self.assertEqual(len(chg_values), 2)

        # both attributes are created
        self.assertEqual([val[1] for val in chg_values], [True, True])

        value_map = {'osm': 'osm val'}
        chg_values = locality.set_values(value_map)

        # attribute has been updated
        self.assertEqual(chg_values[0][1], False)

    def test_set_values_bad_key(self):
        gr = GroupF.create(name='a group')

        AttributeF.create(key='test', in_groups=[gr])
        AttributeF.create(key='osm', in_groups=[gr])

        locality = LocalityF.create(pk=1, group=gr)

        gr2 = GroupF.create(name='a group')
        AttributeF.create(key='osm2', in_groups=[gr2])

        value_map = {'osm2': 'bad key', 'test': 'test val'}
        chg_values = locality.set_values(value_map)

        self.assertEqual(len(chg_values), 1)

    def test_uuid_uniqueness(self):
        LocalityF.create(uuid='test_uuid')

        self.assertRaises(IntegrityError, LocalityF.create, uuid='test_uuid')

    def test_upstream_id_uniqueness(self):
        LocalityF.create(upstream_id='test_id')

        self.assertRaises(
            IntegrityError, LocalityF.create, upstream_id='test_id'
        )

    def test_repr_dict_method(self):
        gr = GroupF.create(name='a group')

        AttributeF.create(key='test', in_groups=[gr])
        AttributeF.create(key='osm', in_groups=[gr])

        locality = LocalityF.create(
            pk=1, group=gr, uuid='93b7e8c4621a4597938dfd3d27659162',
            geom='POINT (16 45)'
        )

        value_map = {'osm': 'osm val', 'test': 'test val'}
        locality.set_values(value_map)

        self.assertDictEqual(locality.repr_dict(), {
            u'id': 1, u'uuid': '93b7e8c4621a4597938dfd3d27659162',
            u'geom': [16, 45],
            u'values': {u'test': u'test val', u'osm': u'osm val'}
        })

    def test_repr_simple_method(self):

        locality = LocalityF.create(pk=1, geom='POINT (16 45)')

        self.assertDictEqual(locality.repr_simple(), {
            u'i': 1, u'g': [16, 45]
        })
