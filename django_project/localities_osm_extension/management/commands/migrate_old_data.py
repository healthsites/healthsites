# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '14/05/19'

import sys
from django.core.management.base import BaseCommand
from localities.models import Locality
from localities_osm.utilities import (
    convert_into_osm_dict,
    split_osm_and_extension_attr
)
from localities_osm_extension.models.extension import LocalityOSMExtension
from localities_osm_extension.models.tag import Tag


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

        print('Start migrating data.........')

        query = Locality.objects.filter(
            changeset__social_user__username=options['username']
        )

        for locality in query:
            values = locality.repr_dict()

            if values.get('osm_id', None):
                print('')
                osm_id = values['osm_id']

                if values.get('osm_type', None):
                    osm_type = values['osm_type']
                else:
                    continue

                print(
                    'Checking locality for osm id: {}, osm type: {}'.format(
                        osm_id, osm_type))

                osm_dict = convert_into_osm_dict(query[0])
                osm, extension = split_osm_and_extension_attr(osm_dict)

                locality_extension, created = \
                    LocalityOSMExtension.objects.get_or_create(
                        osm_id=osm_id,
                        osm_type=osm_type
                    )
                if created:
                    print(
                        'OSM Extension for osm id:{} is created'.format(osm_id))

                for item, value in extension.items():
                    tag, created = Tag.objects.get_or_create(
                        extension=locality_extension,
                        name=item,
                        value=value
                    )
                    if created:
                        print('Tag {}: {} is created'.format(item, value))
                print('')

        print('Migrating old data is finished.')
