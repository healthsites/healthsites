# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from ...importers import CSVImporter


class Command(BaseCommand):
    args = '<group_name> <source_name> <filename> <attr_map_file>'
    help = 'Import Localities from CSV file'

    def handle(self, *args, **options):

        if len(args) != 4:
            raise CommandError('Missing required arguments')

        group_name = args[0]
        source_name = args[1]
        csv_filename = args[2]
        attr_map_file = args[3]

        CSVImporter(group_name, source_name, csv_filename, attr_map_file)
