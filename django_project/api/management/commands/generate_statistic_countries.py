__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from localities.models import Country

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        'This script to generate statistic cache.')

    def handle(self, *args, **options):
        """ Do your work here """
        call_command('generate_statistic_country')
        countries = Country.objects.all()
        for country in countries:
            call_command('generate_statistic_country', country=country.name)
