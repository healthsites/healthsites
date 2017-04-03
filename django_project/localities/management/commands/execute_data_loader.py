# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from localities.tasks import load_data_task


class Command(BaseCommand):
    args = '<data_loader_pk>'
    help = 'Execute data loader'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Missing required arguments')

        loader_pk = args[0]
        load_data_task(loader_pk)
