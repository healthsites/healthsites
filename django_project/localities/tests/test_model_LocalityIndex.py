# -*- coding: utf-8 -*-
from unittest import skip

from django.db import connection
from django.test import TestCase

from ..models import LocalityIndex
from .model_factories import AttributeF, DomainF, LocalityF, SpecificationF, ValueF


class TestModelLocalityIndex(TestCase):
    def test_LocalityIndex_fields(self):
        self.assertListEqual(
            [fld.name for fld in LocalityIndex._meta.fields], [
                u'id', 'locality', 'ranka', 'rankb', 'rankc', 'rankd',
                'fts_index'
            ]
        )

    @skip('skip')
    def test_indexCreation(self):
        attr1 = AttributeF.create(key='test1')
        attr2 = AttributeF.create(key='test2')

        dom = DomainF.create(name='domain')

        spec1 = SpecificationF.create(attribute=attr1, domain=dom)
        spec2 = SpecificationF.create(attribute=attr2, domain=dom)

        loc = LocalityF.create(pk=1, domain=dom)

        ValueF.create(locality=loc, specification=spec1, data='test')
        ValueF.create(locality=loc, specification=spec2, data='test')

        changed_values = {'test1': 'super data', 'test2': 'bad data'}

        # this will trigger index update
        # but it won't https://code.djangoproject.com/ticket/11665)
        loc.set_values(changed_values, loc.changeset.social_user)

        # so we need to do the update manually
        cursor = connection.cursor()
        cursor.execute((
            'UPDATE localities_localityindex SET '
            'fts_index = to_tsvector(\'english\', \'super data bad data\')' # noqa
        ))

        # test LocalityIndex
        search = LocalityIndex.objects.filter(fts_index__search='super')

        self.assertEqual(search.count(), 1)
        self.assertEqual([str(rec.locality) for rec in search], ['1'])
