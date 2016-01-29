# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

import uuid
import json

from django.contrib.gis.geos import Point, Polygon
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Locality, Domain, Changeset

from .exceptions import LocalityImportError

from ._csv_unicode import UnicodeDictReader


class CSVImporter:
    """
    CSV based importer

    Importing a CSV/TSV files requires a:
    * domain name - used to find all associated Specifications
    * name of the source - used to distinguish upstream_ids
    * csv filename
    * attribute mapping file (JSON) - maps csv column names to specifications
    """

    def __init__(
            self, data_loader, domain_name, source_name, csv_filename, attr_json_file,
            use_tabs=False, user=None, mode=1):
        self.data_loader = data_loader
        self.domain_name = domain_name
        self.source_name = source_name
        self.csv_filename = csv_filename
        self.parsed_data = {}
        # Mode
        # 1 : Replace Data
        # 2 : Update Data
        self.mode = mode
        if not user:
            user = get_user_model()
            # Dummy user if not provided.
            self.user = user.objects.get(pk=-1)
        else:
            self.user = user

        self.use_tabs = use_tabs
        self.delta = 0.01

        with open(attr_json_file, 'rb') as attr_map_file:
            self.attr_map = json.load(attr_map_file)

        self.report = {
            'created': 0,
            'modified': 0,
            'duplicated': 0,
            'skipped': 0
        }
        self.exception = None

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

    @staticmethod
    def _find_locality(the_uuid, upstream_id):
        """
        Tries to find a Locality in the database either by *the_uuid* or a
        combination of *source_name* and *upstream_id*

        If there are no results, just create a new Locality
        """

        try:
            # try to find locality by the_uuid or upstream_id
            loc = Locality.objects.filter(uuid=the_uuid).get()
            LOG.debug('Found Locality by the_uuid: %s', the_uuid)
            return loc, False
        except Locality.DoesNotExist:
            try:
                loc = Locality.objects.filter(upstream_id=upstream_id).get()
                LOG.debug('Found Locality by upstream_id: %s', upstream_id)
                return loc, False
            except Locality.DoesNotExist:
                # create new Locality
                loc = Locality()
                LOG.debug('Creating a new Locality')
                return loc, True

    @staticmethod
    def _read_attr(row, attr):
        """
        Try to read attribute from a row
        """

        try:
            return row[attr]
        except KeyError:
            return None

    @staticmethod
    def parse_geom(lon, lat):
        """
        Parse geometry
        """

        try:
            lon = float(lon)
            lat = float(lat)

            # we use EPSG:4326, coordinates are limited by -180/180 -90/90
            if not (-180.0 < lon < 180.0 and -90.0 < lat < 90.0):
                return None
            else:
                return lon, lat
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
        if not row_upstream_id:
            LOG.error('Row %s has no upstream_id, skipping...', row_num)
            # skip this row
            return None

        gen_upstream_id = u'{}¶{}'.format(self.source_name, row_upstream_id)

        if gen_upstream_id in self.parsed_data:
            LOG.error(
                    'Row %s with upstream_id: %s already exists, skipping...',
                    row_num, gen_upstream_id
            )
            self.report['skipped'] += 1
            return None

        tmp_geom = self.parse_geom(
                row_data[self.attr_map['geom'][0]],
                row_data[self.attr_map['geom'][1]]
        )

        if not tmp_geom:
            LOG.error('Row %s has invalid geometry, skipping...', row_num)
            # skip this row
            self.report['skipped'] += 1
            return None

        if tmp_geom == (0, 0):
            LOG.error('Row %s is located in Null Island (0, 0), skipping...', row_num)
            self.report['skipped'] += 1
            return None

        self.parsed_data.update({
            gen_upstream_id: {
                'uuid': row_uuid,
                'upstream_id': gen_upstream_id,
                'geom': tmp_geom,
                'values': {
                    key: self._read_attr(row_data, row_val)
                    for key, row_val in self.attr_map['attributes'].iteritems()
                    if self._read_attr(row_data, row_val) not in (None, '')
                    }
            }
        })

    def save_localities(self):
        """
        Save every locality in the parsed_data dictionary
        """

        # generate a new changeset id
        tmp_changeset = Changeset.objects.create(social_user=self.user)

        for gen_upstream_id, values in self.parsed_data.iteritems():
            row_uuid = values['uuid']
            loc, _created = self._find_locality(row_uuid, gen_upstream_id)

            if _created:
                # finding duplication
                # loc_geom = Point(*values['geom'])
                # loc_envelope = self.envelope(loc_geom.x, loc_geom.y)
                # duplicate_localities = Locality.objects.filter(
                #     geom__within=loc_envelope)
                #
                # if len(duplicate_localities) > 0:
                #     LOG.info('Possible duplicate %s (%s) at (%s, %s)',
                #              loc.uuid, loc.id, loc_geom.x, loc_geom.y)
                #     self.report['duplicated'] += 1
                #     continue

                loc.changeset = tmp_changeset
                loc.domain = self.domain
                loc.uuid = row_uuid or uuid.uuid4().hex  # gen new uuid if None
                loc.upstream_id = gen_upstream_id

                loc.geom = Point(*values['geom'])
                # save Locality
                loc.save()
                LOG.info('Created %s (%s)', loc.uuid, loc.id)

                # save values for Locality
                loc.set_values(values['values'], social_user=self.user)

                self.report['created'] += 1
            else:
                # check location duplication

                # apply mode
                loc.changeset = tmp_changeset
                loc.geom = Point(*values['geom'])

                loc.save()
                LOG.info('Updated %s (%s)', loc.uuid, loc.id)
                if self.mode == 1:
                    # replace
                    # delete old value
                    old_value = loc.repr_dict()['values']
                    for key in old_value.keys():
                        old_value[key] = ''
                    new_value = values['values']

                    merged_value = old_value.copy()
                    merged_value.update(new_value)

                    loc.set_values(merged_value, social_user=self.user)

                elif self.mode == 2:
                    # update
                    # merged old and new value
                    # set merged value
                    old_value = loc.repr_dict()['values']
                    new_value = values['values']
                    merged_value = old_value.copy()
                    merged_value.update(new_value)
                    loc.set_values(merged_value, social_user=self.user)
                else:
                    loc.set_values(values['values'], social_user=self.user)

                self.report['modified'] += 1

            loc.update_history(self.data_loader.date_time_uploaded, self.data_loader.data_loader_mode, self.user);

    def envelope(self, lon, lat):
        """Return polygon envelope for point (lon, lat)
        """
        x_min = lon - self.delta
        x_max = lon + self.delta
        y_min = lat - self.delta
        y_max = lat + self.delta

        polygon = Polygon.from_bbox([x_min, y_min, x_max, y_max])

        return polygon

    def parse_file(self):
        """
        Open a file and parse rows

        All modifications to the database are going to be executed as a single
        transaction to minimize inconsistent database state
        """

        try:
            with open(self.csv_filename, 'rb') as csv_file:
                if self.use_tabs:
                    data_file = UnicodeDictReader(csv_file, delimiter='\t')
                else:
                    data_file = UnicodeDictReader(csv_file)

                with transaction.atomic():
                    for r_num, r_data in enumerate(data_file):
                        self.parse_row(r_num, r_data)
                    # save localities to the database
                    self.save_localities()
        except EnvironmentError as e:
            self.exception = e

    def generate_report(self):
        """Generate report for the import process
        """
        report = 'Report\n\n'
        total = 0
        for i, key in enumerate(sorted(self.report.iterkeys())):
            total += self.report[key]
        for i, key in enumerate(sorted(self.report.iterkeys())):
            if total > 0:
                percentage = 100.0 * self.report[key] / total
            else:
                percentage = 0
            report += ('%s. Number of %s locality is %s (%.2f %%).\n' % (
                i + 1, key, self.report[key], percentage))

        if self.exception:
            report += 'Notes:\n'
            report += self.exception

        return report
