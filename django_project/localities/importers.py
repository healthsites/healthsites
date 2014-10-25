# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import uuid

from django.contrib.gis.geos import Point
from django.db import transaction

from .models import Locality, Group
from .exceptions import LocalityImportError

from ._csv_unicode import UnicodeDictReader


class CSVImporter():

    def __init__(self, group_name, source_name, csv_filename):
        self.group_name = group_name
        self.source_name = source_name
        self.csv_filename = csv_filename

        self.attr_map = {
            'uuid': 'uuid',
            'upstream_id': '_num',
            'geom': ['lat', 'lon'],
            'attributes': {
                'services': 'services',
                'contact-details': 'contact_details',
                'physical-address': 'physical_address',
                'name': 'name',
                'url': '_pageUrl'
            }
        }

        # import
        self._get_group()
        self.parse_file()

    def _get_group(self):
        try:
            self.group = Group.objects.filter(name=self.group_name).get()
        except Group.DoesNotExist:
            msg = 'Group "{}" does not exist'.format(self.group_name)
            LOG.error(msg)
            raise LocalityImportError(msg)

    def _find_locality(self, uuid, upstream_id):
        try:
            # try to find locality by uuid or upstream_id
            loc = Locality.objects.filter(uuid=uuid).get()
            LOG.debug('Found Locality by uuid: %s', uuid)
            return loc
        except Locality.DoesNotExist:
            try:
                loc = Locality.objects.filter(upstream_id=upstream_id).get()
                LOG.debug('Found Locality by upstream_id: %s', upstream_id)
                return loc
            except Locality.DoesNotExist:
                # create new Locality
                loc = Locality()
                LOG.debug('Creating new Locality')
                return loc

    def _read_attr(self, row, attr):
        try:
            return row[attr]
        except KeyError:
            return None

    def parse_row(self, row_num, row_data):
        row_uuid = self._read_attr(row_data, self.attr_map['uuid'])
        row_upstream_id = self._read_attr(
            row_data, self.attr_map['upstream_id']
        )
        if not(row_upstream_id):
            LOG.error('Row {} has no upstream_id, skipping...', row_num)
            # skip this row
            return None

        gen_upstream_id = u'{}¶{}'.format(self.source_name, row_upstream_id)

        loc = self._find_locality(row_uuid, gen_upstream_id)

        loc.group = self.group
        loc.uuid = row_uuid or uuid.uuid4().hex  # gen new uuid if None
        loc.upstream_id = gen_upstream_id
        loc.geom = Point(*map(float, [
            row_data[self.attr_map['geom'][0]],
            row_data[self.attr_map['geom'][1]]
        ]))

        # save Locality
        loc.save()
        LOG.info('Saved %s (%s)', loc.uuid, loc.id)

        # map values to attributes
        value_map = {
            key: self._read_attr(row_data, row_val)
            for key, row_val in self.attr_map['attributes'].iteritems()
        }
        # save values for Locality
        loc.set_values(value_map)

    def parse_file(self):
        with open(self.csv_filename, 'rb') as csv_file:
            with transaction.atomic():
                for r_num, r_data in enumerate(UnicodeDictReader(csv_file)):
                    self.parse_row(r_num, r_data)
