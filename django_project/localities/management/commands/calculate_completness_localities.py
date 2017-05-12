# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from localities.models import Locality


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
