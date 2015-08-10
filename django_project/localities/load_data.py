# coding=utf-8
"""Docstring for this file."""
__author__ = 'ismailsunni'
__project_name = 'healthsites'
__filename = 'load_data.py'
__date__ = '8/7/15'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

from django.db import transaction
from django.contrib.gis.geos import Point, Polygon

import json
import logging
import uuid
LOG = logging.getLogger(__name__)

from _csv_unicode import UnicodeDictReader
from models import DataLoader, Locality, Changeset


class LoadData(object):
    """Class for managing loading data."""

    def __init__(self, data_loader, use_tabs=True, mode=1):
        """
        :param data_loader: A DataLoader object.
        :type data_loader: DataLoader
        """
        self.use_tabs = use_tabs
        self.mode = mode
        self.domain = 'Health'
        self.parsed_data = {}
        self.source_name = data_loader.organisation_name
        self.user = data_loader.author
        self.csv_data_path = data_loader.csv_data.path
        self.delta = 0.01

        with open(
                data_loader.json_concept_mapping.path, 'rb') as attr_map_file:
            self.attr_map = json.load(attr_map_file)

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
            if not(-180.0 < lon < 180.0 and -90.0 < lat < 90.0):
                return None
            else:
                return lon, lat
        except ValueError:
            return None

    def envelope(self, lon, lat):
        """Return polygon envelope for point (lon, lat)
        """
        x_min = lon - self.delta
        x_max = lon + self.delta
        y_min = lat - self.delta
        y_max = lat + self.delta

        polygon = Polygon.from_bbox([x_min, y_min, x_max, y_max])

        return polygon

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

        tmp_geom = self.parse_geom(
            row_data[self.attr_map['geom'][0]],
            row_data[self.attr_map['geom'][1]]
        )
        if not tmp_geom:
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
                    for key, row_val in self.attr_map['attributes'].iteritems()
                    if self._read_attr(row_data, row_val) not in (None, '')
                    }
            }
        })

    def apply(self):
        tmp_changeset = Changeset.objects.create(social_user=self.user)

        for gen_upstream_id, values in self.parsed_data.iteritems():
            pass
            location = values['geom']
            row_uuid = values['uuid']
            bbox = self.envelope(location[0], location[1])
            # find localities near location
            current_localities = Locality.objects.filter(geom__within=bbox)

            if len(current_localities) > 0:
                # match, not creating new localities
                # updating the first match
                locality = current_localities[0]

                locality.changeset = tmp_changeset
                locality.geom = Point(*values['geom'])

                locality.save()
                LOG.info('Updated %s (%s)', locality.uuid, locality.id)
                locality.set_values(values['values'], social_user=self.user)

                for current_locality in current_localities[1:]:
                    # delete ?
                    LOG.info('Delete duplicate locality %s (%s)',
                             current_locality.uuid, current_locality.id)
                    current_locality.delete()

            else:
                # not match, creating new localities
                new_locality = Locality()
                new_locality.changeset = tmp_changeset
                new_locality.domain = self.domain
                # gen new uuid if None
                new_locality.uuid = row_uuid or uuid.uuid4().hex
                new_locality.geom = Point(*values['geom'])

                # save Locality
                new_locality.save()
                LOG.info('Created new locality %s (%s)',
                         new_locality.uuid, new_locality.id)

                # save values for Locality
                new_locality.set_values(
                    values['values'], social_user=self.user)

    def run(self):
        """Load the data."""

        with open(self.csv_data_path, 'rb') as csv_file:
            if self.use_tabs:
                data_file = UnicodeDictReader(csv_file, delimiter='\t')
            else:
                data_file = UnicodeDictReader(csv_file)

            with transaction.atomic():
                for r_num, r_data in enumerate(data_file):
                    self.parse_row(r_num, r_data)
                # Apply loading
                self.apply()
