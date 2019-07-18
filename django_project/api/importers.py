# -*- coding: utf-8 -*-
import csv
import json
import logging
import sys

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from api.osm_field_definitions import ALL_FIELDS
from api.osm_tag_defintions import ALL_TAGS
from api.utils import remap_dict, verify_user, validate_osm_data, \
    convert_to_osm_tag, create_osm_node
from core.settings.utils import ABS_PATH
from localities_osm.utilities import split_osm_and_extension_attr

LOG = logging.getLogger(__name__)


class CSVtoOSMImporter:
    """CSV Based Importer"""

    def __init__(self, data_loader, csv_filename, mapping_filename):
        self.data_loader = data_loader
        self.csv_filename = csv_filename
        self._fields = []
        self._parsed_data = []
        self._validation_status = {}
        self._upload_status = {}

        with open(mapping_filename, 'rb') as mapping_file:
            self.json_mapping = json.load(mapping_file)

        self.parse_file()
        self.validate_data() and self.upload_to_osm()

    def fields(self):
        """Get all fields from csv based on mapping file.

        :return: Field names
        :rtype: dict
        """
        return self._fields

    def parsed_data(self):
        """Get parsed data which has been mapped and converted to comply with
        OSM push data payload.

        :return: Parsed data
        :rtype: dict
        """
        return self._parsed_data

    def validation_status(self):
        """Get validation status per data (per row in csv).

        :return: Validation status
        :rtype: dict
        """
        return self._validation_status

    def is_valid(self):
        """Check if all data is valid or not.

        :return: Validation flag
        :rtype: bool
        """
        return False not in (
            [status['is_valid'] for status in
             self._validation_status.values()])

    def upload_status(self):
        """Get upload status.

        :return: Upload status
        :rtype: dict
        """
        return self._upload_status

    def is_uploaded(self):
        """Check if all data is uploaded or not.

        :return: Upload flag
        :rtype: bool
        """
        return False not in (
            [status['is_valid'] for status in
             self._upload_status.values()])

    def import_status(self):
        """Get status of the import process.

        :return: CSV import status
        :rtype: dict
        """
        return (
            self._validation_status if (
                not self.is_valid()) else self._upload_status)

    def is_applied(self):
        """Check if there is applied data or not.

        :return: Applied flag
        :rtype: bool
        """
        return True in (
            [status['uploaded'] for status in
             self._upload_status.values()])

    def parse_file(self):
        """Open a file and parse rows.

        Parsing data are done using json mapping file as a reference.
        """
        # Read csv file as a dict and then remap it to osm fields
        with open(self.csv_filename, 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self._parsed_data.append(
                    remap_dict(
                        row, {y: x for x, y in self.json_mapping.iteritems()}))

        # Rearrange it to osm api push data format
        new_parsed_data = []
        for data in self._parsed_data:
            new_data = dict(data)
            new_data['tag'] = {}
            for key in data:
                if key in [tag['key'] for tag in ALL_TAGS]:
                    new_data['tag'].update({key: data[key]})
                    del new_data[key]

            new_parsed_data.append(new_data)

        self._parsed_data = new_parsed_data

    def validate_data(self):
        """Validate parsed data based on healthsites rules.

        :return: Flag indicating whether the data is valid or not.
        :rtype: bool
        """
        for row_number, data in enumerate(self._parsed_data):
            validation_status = {
                'is_valid': True,
                'message': ''
            }

            # Set default user to data loader author
            user = self.data_loader.author

            # Split osm and extension attribute
            osm_attr, locality_attr = split_osm_and_extension_attr(
                data['tag'])
            data['tag'] = osm_attr

            # Verify data uploader and owner/collector if the API is being used
            # for uploading data from other osm user.
            if data.get('osm_user') and user.username != data.get('osm_user'):
                is_valid, message = verify_user(user, data['osm_user'])
                validation_status.update({
                    'is_valid': is_valid,
                    'message': message
                })
                if is_valid:
                    try:
                        user = get_object_or_404(
                            User, username=data['osm_user'])
                    except Http404:
                        message = 'User %s is not exist.' % data['osm_user']
                        validation_status.update({
                            'is_valid': False,
                            'message': message
                        })

            if is_valid:
                # Validate data
                is_valid, message = validate_osm_data(user, data)
                validation_status.update({
                    'is_valid': is_valid,
                    'message': message
                })

            self._validation_status[row_number+1] = validation_status

        return False not in (
            [status['is_valid'] for status in
             self._validation_status.values()])

    def upload_to_osm(self):
        """Push parsed localities/facilities/healthsites data to OSM instance.

        """
        for row_number, data in enumerate(self._parsed_data):
            upload_status = {
                'uploaded': True,
                'message': ''
            }

            # Map Healthsites tags to OSM tags
            mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
            data['tag'] = convert_to_osm_tag(
                mapping_file_path, data['tag'], 'node')

            # Push data to OSM
            user = get_object_or_404(User, username=data['osm_user'])
            try:
                _ = create_osm_node(user, data)
            except:  # noqa
                upload_status.update({
                    'uploaded': False,
                    'message': "{0}: {1}".format(
                        unicode(sys.exc_info()[0].__name__),
                        unicode(sys.exc_info()[1]))
                })

            self._upload_status[row_number+1] = upload_status

        return False not in (
            [status['uploaded'] for status in
             self._upload_status.values()])

    def generate_report(self):
        """Generate report for the import process
        """
        report = ''
        for row_number, status in self.import_status().items():
            if status.get('uploaded', status.get('is_valid')):
                report += 'Row %s success. ' % row_number
            else:
                report += 'Row %s failed. ' % row_number
            report += '%s\n' % status['message']

        return report

    @staticmethod
    def generate_mapping_template():
        """Generate fields mapping template.

        :return: Fields mapping template
        :rtype: dict
        """
        mapping_template = {}
        for field_definition in ALL_FIELDS + ALL_TAGS:
            mapping_template[field_definition['key']] = ''

        return mapping_template
