__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/04/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'
# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import Localities from CSV file'

    def handle(self, *args, **options):
        print "---------------------------------------------"
        print "call generate countries"
        print "---------------------------------------------"
        call_command('generate_countries')
        print "---------------------------------------------"
        print "call generate masterization by cluster"
        print "---------------------------------------------"
        call_command('generate_masterization_by_cluster', 48, 46)
        print "---------------------------------------------"
        print "call gen_cluster_cache"
        print "---------------------------------------------"
        call_command('gen_cluster_cache', 48, 46)
        print "---------------------------------------------"
        print "call generate countries cache"
        print "---------------------------------------------"
        call_command('generate_countries_cache')
