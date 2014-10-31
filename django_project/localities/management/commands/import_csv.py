# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...importers import CSVImporter


class Command(BaseCommand):

    args = '<domain_name> <source_name> <filename> <attr_map_file>'
    help = 'Import Localities from CSV file'

    option_list = BaseCommand.option_list + (
        make_option(
            '--tabs', action='store_true', dest='use_tabs', default=False,
            help='Use when input file is tab delimited'
        ),
    )

    def handle(self, *args, **options):

        if len(args) != 4:
            raise CommandError('Missing required arguments')

        domain_name = args[0]
        source_name = args[1]
        csv_filename = args[2]
        attr_map_file = args[3]

        CSVImporter(
            domain_name, source_name, csv_filename, attr_map_file,
            options["use_tabs"]
        )
