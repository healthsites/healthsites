# -*- coding: utf-8 -*-
from django.test import TestCase

from django.db import IntegrityError

from social_users.tests.model_factories import UserF

from .model_factories import (
    LocalityF,
    LocalityValue1F,
    AttributeF,
    DomainSpecification1AF,
    DomainSpecification2AF,
    ChangesetF
)


class TestModelLocality(TestCase):
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
            list(locality.get_attr_map()), [
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

    def test_repr_dict_method(self):
        user = UserF(username='test', password='test')
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

        chgset = ChangesetF.create(social_user=user)

        locality = LocalityF.create(
            pk=1, domain=dom, uuid='93b7e8c4621a4597938dfd3d27659162',
            geom='POINT (16 45)', changeset=chgset
        )

        value_map = {'osm': 'osm val', 'test': 'test val'}
        locality.set_values(value_map, social_user=user)

        self.assertDictEqual(locality.repr_dict(), {
            u'id': 1, u'uuid': '93b7e8c4621a4597938dfd3d27659162',
            u'geom': (16, 45),
            u'values': {u'test': u'test val', u'osm': u'osm val'}
        })

    def test_repr_simple_method(self):

        locality = LocalityF.create(pk=1, geom='POINT (16 45)')

        self.assertDictEqual(locality.repr_simple(), {
            u'i': 1, u'g': [16, 45]
        })

    def test_set_geom_method(self):
        loc = LocalityF.create(pk=1, geom='POINT (16 45)')
        loc.set_geom(10.0, 35.0)
        loc.save()

        self.assertDictEqual(loc.repr_simple(), {
            u'i': 1, u'g': [10.0, 35.0]
        })
