# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import uuid
import json
import csv

from django.contrib.gis.geos import Point
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Locality, Domain, Changeset

from .exceptions import LocalityImportError


class CSVImporter():
    """
    CSV based importer

    Importing a CSV/TSV files requires a:
    * domain name - used to find all associated Specifications
    * name of the source - used to distinguish upstream_ids
    * csv filename
    * attribute mapping file (JSON) - maps csv column names to specifications
    """

    parsed_data = {}

    def __init__(
            self, domain_name, source_name, csv_filename, attr_json_file,
            use_tabs=False):
        self.domain_name = domain_name
        self.source_name = source_name
        self.csv_filename = csv_filename

        self.use_tabs = use_tabs

        with open(attr_json_file, 'r') as attr_map_file:
            self.attr_map = json.load(attr_map_file)

        # import
        self._get_domain()
        self.parse_file()

    def _get_domain(self):
        """
        Retrieves a domain from the database
        """

        try:
            self.domain = Domain.objects.filter(name=self.domain_name).get()
        except Domain.DoesNotExist:
            msg = 'Domain "{}" does not exist'.format(self.domain_name)
            LOG.error(msg)
            raise LocalityImportError(msg)

    def _find_locality(self, uuid, upstream_id):
        """
        Tries to find a Locality in the database either by *uuid* or a
        combination of *source_name* and *upstream_id*

        If there are no results, just create a new Locality
        """

        try:
            # try to find locality by uuid or upstream_id
            loc = Locality.objects.filter(uuid=uuid).get()
            LOG.debug('Found Locality by uuid: %s', uuid)
            return (loc, False)
        except Locality.DoesNotExist:
            try:
                loc = Locality.objects.filter(upstream_id=upstream_id).get()
                LOG.debug('Found Locality by upstream_id: %s', upstream_id)
                return (loc, False)
            except Locality.DoesNotExist:
                # create new Locality
                loc = Locality()
                LOG.debug('Creating a new Locality')
                return (loc, True)

    def _read_attr(self, row, attr):
        """
        Try to read attribute from a row
        """

        try:
            return row[attr]
        except KeyError:
            return None

    def parse_geom(self, lon, lat):
        """
        Parse geometry
        """

        try:
            lon = float(lon)
            lat = float(lat)

            # we use EPSG:4326, coordinates are limited by -180/180 -90/90
            if not(-180.0 < lon < 180.0 and -90.0 < lat < 90.0):
                return None
            else:
                return (lon, lat)
        except ValueError:
            return None

    def parse_row(self, row_num, row_data):
        """
        Parse row of data and add it to the *parsed_data* dictionary
        """

        row_uuid = self._read_attr(row_data, self.attr_map['uuid'])
        row_upstream_id = self._read_attr(
            row_data, self.attr_map['upstream_id']
        )
        if not(row_upstream_id):
            LOG.error('Row %s has no upstream_id, skipping...', row_num)
            # skip this row
            return None

        gen_upstream_id = u'{}¶{}'.format(self.source_name, row_upstream_id)

        if gen_upstream_id in self.parsed_data:
            LOG.error(
                'Row %s with upstream_id: %s already exists, skipping...',
                row_num, gen_upstream_id
            )

        tmp_geom = self.parse_geom(
            row_data[self.attr_map['geom'][0]],
            row_data[self.attr_map['geom'][1]]
        )
        if not(tmp_geom):
            LOG.error('Row %s has invalid geometry, skipping...', row_num)
            # skip this row
            return None

        self.parsed_data.update({
            gen_upstream_id: {
                'uuid': row_uuid,
                'upstream_id': gen_upstream_id,
                'geom': tmp_geom,
                'values': {
                    key: self._read_attr(row_data, row_val)
                    for key, row_val in self.attr_map['attributes'].items()
                    if self._read_attr(row_data, row_val) not in (None, '')
                }
            }
        })

    def save_localities(self):
        """
        Save every locality in the parsed_data dictionary
        """

        # generate a new changeset id
        User = get_user_model()

        # TODO: use real user for import, at the moment we use a dummy user
        dummy_user = User.objects.get(pk=-1)
        tmp_changeset = Changeset.objects.create(social_user=dummy_user)

        for gen_upstream_id, values in self.parsed_data.items():
            row_uuid = values['uuid']
            loc, _created = self._find_locality(row_uuid, gen_upstream_id)

            if _created:
                loc.changeset = tmp_changeset
                loc.domain = self.domain
                loc.uuid = row_uuid or uuid.uuid4().hex  # gen new uuid if None
                loc.upstream_id = gen_upstream_id

                loc.geom = Point(*values['geom'])
                # save Locality
                loc.save()
                LOG.info('Created %s (%s)', loc.uuid, loc.id)

                # save values for Locality
                loc.set_values(values['values'], social_user=dummy_user)
            else:
                loc.changeset = tmp_changeset
                loc.geom = Point(*values['geom'])

                loc.save()
                LOG.info('Updated %s (%s)', loc.uuid, loc.id)
                loc.set_values(values['values'], social_user=dummy_user)

    def parse_file(self):
        """
        Open a file and parse rows

        All modifications to the database are going to be executed as a single
        transaction to minimize inconsistent database state
        """

        with open(self.csv_filename, 'r', encoding='utf-8') as csv_file:
            if self.use_tabs:
                data_file = csv.DictReader(csv_file, delimiter='\t')
            else:
                data_file = csv.DictReader(csv_file)

            with transaction.atomic():
                for r_num, r_data in enumerate(data_file):
                    self.parse_row(r_num, r_data)
                # save localities to the database
                self.save_localities()
