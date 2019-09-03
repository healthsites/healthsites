# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '14/05/19'

import json
import os
import sys
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from localities.models import Locality
from localities_osm.utilities import (
    convert_into_osm_dict,
    split_osm_and_extension_attr
)
from localities_osm_extension.utils import save_extensions
from api.api_views.v2.utilities import create_osm_node_by_data


class Command(BaseCommand):
    """
    This command converts old data to osm and save
    the additional attributes as osm extension.

    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            help='Filter locality by username',
        )

    def handle(self, *args, **options):
        if not options['username']:
            sys.exit(
                'Please provide username parameter by adding '
                '--username=<username>')
            return

        try:
            user = User.objects.get(username=options['username'])
        except User.DoesNotExist:
            sys.exit(
                'Username does not exist')
            return

        pathname = \
            os.path.join(settings.CACHE_DIR, 'data-migration-progress')
        progress_file = \
            os.path.join(pathname, '{}.txt'.format(options['username']))
        progress_file_found = os.path.exists(progress_file)

        if progress_file_found:
            sys.exit(
                'Data migration process for user {} '
                'is already running.'.format(options['username']))

        print('Start migrating data.........')

        query = Locality.objects.filter(
            changeset__social_user__username=options['username']
        )

        total_query = query.count()
        for idx, locality in enumerate(query):

            # change into osm format
            osm_dict = convert_into_osm_dict(locality)
            osm, extension = split_osm_and_extension_attr(osm_dict)

            values = locality.repr_dict()
            if values.get('osm_id', None):
                if values.get('osm_type', None):
                    osm_type = values['osm_type']
                else:
                    continue

                osm_id = values['osm_id']

                print(
                    'Checking locality for osm id: {}, osm type: {}'.format(
                        osm_id, osm_type))
                save_extensions(osm_type, osm_id, extension)
            else:
                request_data = osm.copy()
                request_data.update(extension)
                data = {
                    'tag': request_data,
                    "lat": values['geom'][1],
                    "lon": values['geom'][0]
                }
                create_osm_node_by_data(user=user, data=data)

            locality.migrated = True
            locality.save()

            found = os.path.exists(pathname)

            if not found:
                os.makedirs(pathname)

            data_counter = {
                'count': idx + 1,
                'total': total_query,
            }
            filename = os.path.join(pathname, '{}.txt'.format(options['username']))
            f = open(filename, 'w+')
            f.write(json.dumps(data_counter))
            f.close()

        print('Migrating old data is finished.')
