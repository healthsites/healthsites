# -*- coding: utf-8 -*-
from unittest import skip

from django.db import IntegrityError
from django.test import TestCase

from social_users.tests.model_factories import UserF

from ..models import Locality
from .model_factories import (
    AttributeF, ChangesetF, DomainSpecification1AF, DomainSpecification2AF,
    DomainSpecification4AF, LocalityF, LocalityValue1F, LocalityValue4F
)


class TestModelLocality(TestCase):
    def test_Locality_fields(self):
        self.assertListEqual(
            [fld.name for fld in Locality._meta.fields], [
                u'id', 'changeset', 'version', 'domain', 'uuid', 'upstream_id',
                'geom', 'name', 'source', 'migrated', 'completeness',
                'is_master'
            ]
        )

    def test_model_repr(self):
        locality = LocalityF.create(pk=1)

        self.assertEqual(unicode(locality), u'1')

    def test_model_with_value(self):
        attr = AttributeF.create(key='test')
        locality = LocalityValue1F.create(
            pk=1, val1__data='test', val1__specification__attribute=attr
        )

        self.assertEqual(unicode(locality), u'1')
        self.assertEqual(
            [unicode(val) for val in locality.value_set.all()],
            [u'(1) test=test']
        )

    def test_model_uuid_persistnace(self):
        locality = LocalityF.create(uuid='uuid_original')

        locality.uuid = 'uuid_test'
        locality.save()

        self.assertEqual(locality.uuid, 'uuid_original')

    def test_get_attr_map(self):
        attr1 = AttributeF.create(key='test')
        attr2 = AttributeF.create(key='osm')

        dom = DomainSpecification2AF.create(
            name='a domain', spec1__id=1, spec1__attribute=attr1,
            spec2__id=2, spec2__attribute=attr2
        )

        # this domain should not be in results
        attr3 = AttributeF.create(key='osm2')
        DomainSpecification1AF.create(
            name='a new domain', spec1__attribute=attr3, spec1__id=-1
        )

        locality = LocalityF.create(domain=dom)

        self.assertEqual(
            list(locality._get_attr_map()), [
                {'id': 1, 'attribute__key': u'test'},
                {'id': 2, 'attribute__key': u'osm'}
            ]
        )

    def test_set_values(self):
        user = UserF(username='test', password='test')
        attr1 = AttributeF.create(id=1, key='test')
        attr2 = AttributeF.create(id=2, key='osm')

        dom = DomainSpecification2AF.create(
            name='a domain', spec1__attribute=attr1, spec2__attribute=attr2
        )

        chgset = ChangesetF.create(social_user=user)

        locality = LocalityF.create(pk=1, domain=dom, changeset=chgset)

        value_map = {'osm': 'osm val', 'test': 'test val'}
        chg_values = locality.set_values(value_map, social_user=user)

        self.assertEqual(len(chg_values), 2)

        # both attributes are created
        self.assertEqual([val[1] for val in chg_values], [True, True])

        # changesets should be the same for all changed values
        self.assertEqual(
            chg_values[0][0].changeset, chg_values[1][0].changeset
        )
        value_map = {'osm': 'new osm val'}
        chg_values = locality.set_values(value_map, social_user=user)

        # attribute has been updated
        self.assertEqual(chg_values[0][1], False)

    def test_set_values_partial(self):
        user = UserF(username='test', password='test')
        attr1 = AttributeF.create(id=1, key='test')
        attr2 = AttributeF.create(id=2, key='osm')

        dom = DomainSpecification2AF.create(
            name='a domain', spec1__attribute=attr1, spec2__attribute=attr2
        )

        chgset = ChangesetF.create(social_user=user)

        locality = LocalityF.create(pk=1, domain=dom, changeset=chgset)

        value_map = {'osm': 'osm val'}
        chg_values = locality.set_values(value_map, social_user=user)
        self.assertEqual(len(chg_values), 1)

        # is attribute created
        self.assertEqual([val[1] for val in chg_values], [True])

    def test_set_values_bad_key(self):
        user = UserF(username='test', password='test')
        attr1 = AttributeF.create(id=1, key='test')
        attr2 = AttributeF.create(id=2, key='osm')

        chgset = ChangesetF.create(social_user=user)

        dom = DomainSpecification2AF.create(
            name='a domain', spec1__attribute=attr1, spec2__attribute=attr2
        )

        locality = LocalityF.create(pk=1, domain=dom, changeset=chgset)

        value_map = {'osm2': 'bad key', 'test': 'test val'}
        chg_values = locality.set_values(value_map, social_user=user)

        self.assertEqual(len(chg_values), 1)

    def test_uuid_uniqueness(self):
        LocalityF.create(uuid='test_uuid')

        self.assertRaises(IntegrityError, LocalityF.create, uuid='test_uuid')

    def test_upstream_id_uniqueness(self):
        LocalityF.create(upstream_id='test_id')

        self.assertRaises(
            IntegrityError, LocalityF.create, upstream_id='test_id'
        )

    @skip('skip')
    def test_repr_dict_method(self):
        user = UserF(username='test', password='test')
        chgset = ChangesetF.create(id=1, social_user=user)
        attr1 = AttributeF.create(key='test')
        attr2 = AttributeF.create(key='osm')

        dom = DomainSpecification2AF.create(
            name='a domain', spec1__attribute=attr1, spec2__attribute=attr2
        )

        # this domain should not be in results
        attr3 = AttributeF.create(key='osm2')
        DomainSpecification1AF.create(
            name='a new domain', spec1__attribute=attr3
        )

        locality = LocalityF.create(
            pk=1, domain=dom, uuid='93b7e8c4621a4597938dfd3d27659162',
            geom='POINT (16 45)', changeset=chgset
        )

        value_map = {'osm': 'osm val', 'test': 'test val'}
        locality.set_values(value_map, social_user=user)

        self.assertDictEqual(locality.repr_dict(), {
            u'geom': (16.0, 45.0), u'version': 1, u'changeset': 1,
            u'values': {u'test': u'test val', u'osm': u'osm val'},
            u'uuid': '93b7e8c4621a4597938dfd3d27659162'
        })

    def test_set_geom_method(self):
        loc = LocalityF.create(pk=1, geom='POINT (16 45)')
        loc.set_geom(10.0, 35.0)
        loc.save()

        self.assertEqual(
            loc.geom.wkt, 'POINT (10.0000000000000000 35.0000000000000000)'
        )

    def test_prepare_for_fts(self):
        attr1 = AttributeF.create(id=1, key='test1')
        attr2 = AttributeF.create(id=2, key='test2')
        attr3 = AttributeF.create(id=3, key='test3')
        attr4 = AttributeF.create(id=4, key='test4')

        dom = DomainSpecification4AF.create(
            name='a domain', spec1__attribute=attr1, spec1__fts_rank='A',
            spec2__attribute=attr2, spec2__fts_rank='B',
            spec3__attribute=attr3, spec3__fts_rank='C',
            spec4__attribute=attr4, spec4__fts_rank='D'
        )

        locality = LocalityValue4F.create(
            domain=dom, val1__data='1test', val2__data='2test',
            val3__data='3test', val4__data='4test',
            val1__specification=attr1.specification_set.all()[0],
            val2__specification=attr2.specification_set.all()[0],
            val3__specification=attr3.specification_set.all()[0],
            val4__specification=attr4.specification_set.all()[0]
        )

        self.assertEqual(locality.prepare_for_fts(), {
            u'A': u'1test', u'C': u'3test', u'B': u'2test', u'D': u'4test'
        })

    def test_prepare_for_fts_grouping(self):
        attr1 = AttributeF.create(id=1, key='test1')
        attr2 = AttributeF.create(id=2, key='test2')
        attr3 = AttributeF.create(id=3, key='test3')
        attr4 = AttributeF.create(id=4, key='test4')

        dom = DomainSpecification4AF.create(
            name='a domain', spec1__attribute=attr1, spec1__fts_rank='A',
            spec2__attribute=attr2, spec2__fts_rank='A',
            spec3__attribute=attr3, spec3__fts_rank='D',
            spec4__attribute=attr4, spec4__fts_rank='D'
        )

        locality = LocalityValue4F.create(
            domain=dom, val1__data='1test', val2__data='2test',
            val3__data='3test', val4__data='4test',
            val1__specification=attr1.specification_set.all()[0],
            val2__specification=attr2.specification_set.all()[0],
            val3__specification=attr3.specification_set.all()[0],
            val4__specification=attr4.specification_set.all()[0]
        )

        self.assertEqual(locality.prepare_for_fts(), {
            u'A': u'1test 2test', u'D': u'3test 4test'
        })
