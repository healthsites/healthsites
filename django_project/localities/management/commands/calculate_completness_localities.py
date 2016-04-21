# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/04/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.core.management.base import BaseCommand
from localities.models import Locality, Value


class Command(BaseCommand):
    help = 'Clean localities'

    def handle(self, *args, **options):
        loc_count = Locality.objects.all().count()
        index = 1
        for locality in Locality.objects.all():
            print "%d / %d" % (index, loc_count)
            locality.completeness = locality.calculate_completeness()
            locality.save()
            index += 1
