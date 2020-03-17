# -*- coding: utf-8 -*-
import copy
import csv
import json
import logging
import os
import sys

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from api.osm_field_definitions import ALL_FIELDS
from api.osm_tag_defintions import ALL_TAGS
from api.utils import verify_user, validate_osm_data, \
    convert_to_osm_tag, create_osm_node
from api.utilities.pending import create_pending_update
from core.settings.utils import ABS_PATH
from localities_osm_extension.utils import save_extensions
from localities_osm.utilities import split_osm_and_extension_attr

LOG = logging.getLogger(__name__)


class CSVtoOSMImporter:
    """CSV Based Importer"""

    def __init__(
            self, data_loader, csv_filename):
        self.data_loader = data_loader
        self.csv_filename = csv_filename
        self._fields = []
        self._parsed_data = []

        self._validation_status = {
            'status': {},
            'summary': ''
        }
        self._upload_status = {
            'status': {},
            'summary': ''
        }

        self.parse_file()

        # log progress into a file
        self.pathname = os.path.join(settings.CACHE_DIR, 'csv-import-progress')
        self.progress_file = os.path.join(
            self.pathname, '{}.txt'.format(data_loader.author.username))

        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)
        if not os.path.exists(self.pathname):
            os.makedirs(self.pathname)

        if self.validate_data():
            self.upload_to_osm()

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
             self._validation_status['status'].values()])

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
            [status['uploaded'] for status in
             self._upload_status['status'].values()])

    def import_status(self):
        """Get status of the import process.

        :return: CSV import status
        :rtype: dict
        """
        return (
            self._validation_status['status'] if (
                not self.is_valid()) else self._upload_status['status'])

    def is_applied(self):
        """Check if there is applied data or not.

        :return: Applied flag
        :rtype: bool
        """
        try:
            return True in (
                [status['uploaded'] for status in
                 self._upload_status['status'].values()])
        except KeyError:
            return False

    def parse_file(self):
        """Open a file and parse rows.

        Parsing data are done using json mapping file as a reference.
        """
        # Read csv file as a dict and then remap it to osm fields
        with open(self.csv_filename, 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self._parsed_data.append(
                    {
                        key.decode('utf-8-sig').encode('utf-8'):
                            value for key, value in row.iteritems()
                    }
                )

        # Rearrange it to osm api push data format
        new_parsed_data = []
        for data in self._parsed_data:
            new_data = {}
            try:
                new_data['lat'] = data['lat']
                new_data['lon'] = data['lon']
                new_data['osm_user'] = data['osm_user']
                del data['osm_user']
                del data['lat']
                del data['lon']
            except KeyError:
                pass
            new_data['tag'] = data
            new_parsed_data.append(new_data)

        self._parsed_data = new_parsed_data

    def validate_data(self):
        """Validate parsed data based on healthsites rules.

        :return: Flag indicating whether the data is valid or not.
        :rtype: bool
        """
        self._validation_status['total'] = len(self._parsed_data)
        for row_number, data in enumerate(self._parsed_data):
            is_valid = True
            validation_status = {
                'is_valid': is_valid,
                'message': 'Valid'
            }

            # check 2nd row based on the hxl
            if row_number == 0 and 'lat' in data and '#' in data['lat']:
                mapping_file_path = ABS_PATH('api', 'fixtures', 'hxl_tags.json')
                _file = open(mapping_file_path, 'r')
                hxl_tag = json.loads(_file.read())
                _file.close()

                # get the newest hxl tag
                all_tag = copy.deepcopy(data['tag'])
                all_tag['lon'] = data['lon']
                all_tag['lat'] = data['lat']

                for tag, hxl in all_tag.items():
                    try:
                        hxl_tag[tag]
                    except KeyError:
                        hxl_tag[tag] = hxl
                _file = open(mapping_file_path, 'w')
                _file.write(json.dumps(hxl_tag, indent=4))
                _file.close()
                continue

            # Set default user to data loader author
            user = self.data_loader.author

            # Split osm and extension attribute
            osm_attr, locality_attr = split_osm_and_extension_attr(
                data['tag'])
            data['tag'] = osm_attr
            data['tag'].update(locality_attr)

            # Verify data uploader and owner/collector if the API is being used
            # for uploading data from other osm user.
            if not data.get('osm_user'):
                data['osm_user'] = user.username

            if user.username != data.get('osm_user'):
                is_valid, message = verify_user(
                    user, data['osm_user'], ignore_uploader_staff=True)
                validation_status.update({
                    'is_valid': is_valid,
                    'message': message
                })
                if is_valid:
                    try:
                        _ = get_object_or_404(
                            User, username=data['osm_user'])
                    except Http404:
                        message = 'User %s is not exist.' % data['osm_user']
                        validation_status.update({
                            'is_valid': False,
                            'message': message
                        })

            if is_valid:
                try:
                    # Validate data
                    is_valid = validate_osm_data(data)
                    validation_status.update({
                        'is_valid': is_valid,
                        'message': 'OSM data is valid.'
                    })
                except Exception as e:
                    validation_status.update({
                        'is_valid': False,
                        'message': '%s' % e
                    })

            self._validation_status['status'][row_number + 1] = validation_status
            if self.is_valid() and row_number + 1 == len(self._parsed_data):
                # prepare for the next step, upload data
                self._validation_status['count'] = row_number
            else:
                self._validation_status['count'] = row_number + 1

            self._validation_status['summary'] = (
                'Validation failed. Please see the status detail for more '
                'information.' if not self.is_valid() else ''
            )

            # write status to progress file
            f = open(self.progress_file, 'w+')
            f.write(json.dumps(self._validation_status))
            f.close()

        del self._parsed_data[0]
        return False not in (
            [status['is_valid'] for status in
             self._validation_status['status'].values()])

    def upload_to_osm(self):
        """Push parsed localities/facilities/healthsites data to OSM instance.

        """
        self._upload_status['total'] = len(self._parsed_data)
        for row_number, data in enumerate(self._parsed_data):
            upload_status = {
                'uploaded': True,
                'message': 'Uploaded'
            }

            # split osm and extension attributes
            osm_attr, locality_attr = split_osm_and_extension_attr(
                data['tag'])
            data['tag'] = osm_attr

            # Map Healthsites tags to OSM tags
            mapping_file_path = ABS_PATH('api', 'fixtures', 'mapping.yml')
            data['tag'] = convert_to_osm_tag(
                mapping_file_path, data['tag'], 'node')

            # Push data to OSM
            user = get_object_or_404(User, username=data['osm_user'])
            try:
                response = create_osm_node(user, data)

                # create pending index
                create_pending_update(
                    'node', response['id'],
                    data['tag']['name'], user, response['version'])
                save_extensions('node', response['id'], locality_attr)
            except:  # noqa
                upload_status.update({
                    'uploaded': False,
                    'message': '{0}: {1}'.format(
                        unicode(sys.exc_info()[0].__name__),
                        unicode(sys.exc_info()[1]))
                })

            self._upload_status['status'][row_number + 1] = upload_status
            self._upload_status['count'] = row_number + 1

            self._upload_status['summary'] = (
                'There is error when uploading the data. '
                'Please see the status detail for more '
                'information.' if not self.is_uploaded() else ''
            )

            # write status to progress file
            f = open(self.progress_file, 'w+')
            f.write(json.dumps(self._upload_status))
            f.close()

        return False not in (
            [status['uploaded'] for status in
             self._upload_status['status'].values()])

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
