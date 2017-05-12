# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from localities.models import Locality, Value


class Command(BaseCommand):
    help = 'Clean localities'

    def handle(self, *args, **options):
        # cleaning localities that don't have raw source
        # (except OSM and web that created by user)
        incorrect_localities_count = 0
        # get locality that don't have raw sourc
        localities_with_raw_data = (
            Value.objects
            .filter(specification__attribute__key='raw_source')
            .exclude(data__isnull=True)
            .exclude(data__exact='')
            .values('locality')
        )

        # get incorrect locality that :
        # - don't have raw dara
        # - not openstreetmap
        # - not web
        incorrect_localities = (
            Locality.objects
            .exclude(id__in=localities_with_raw_data)
            .exclude(upstream_id__contains='openstreetmap¶')
            .exclude(upstream_id__contains='web¶')
        )
        for locality in incorrect_localities:
            dict = locality.repr_dict()
            upstream = locality.upstream_id.encode('utf-8')
            if "raw_source" not in dict["values"]:
                incorrect_localities_count += 1
                locality.delete()
            print upstream + " : " + locality.uuid.encode('utf-8')

        # get correct locality to be reported
        correct_localities = Locality.objects.filter(id__in=localities_with_raw_data)
        print "--------------------------------------------"
        print "CORRECT LOCALITIES : %d " % correct_localities.count()
        print "--------------------------------------------"
        print "INCORRECT LOCALITIES : %d " % incorrect_localities.count()
        print "--------------------------------------------"
        print "INCORRECT LOCALITIES THAT DELETED : %d " % incorrect_localities_count
        print "--------------------------------------------"
