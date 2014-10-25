# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from ...importers import CSVImporter


class Command(BaseCommand):
    args = '<group_name> <source_name> <filename>'
    help = 'Import Localities from CSV file'

    def handle(self, *args, **options):

        if len(args) != 3:
            raise CommandError('Missing required arguments')

        group_name = args[0]
        source_name = args[1]
        csv_filename = args[2]

        CSVImporter(group_name, source_name, csv_filename)
