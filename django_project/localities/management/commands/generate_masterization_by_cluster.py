# -*- coding: utf-8 -*-
from optparse import make_option

from core.utilities import extract_time
from django.core.management.base import BaseCommand, CommandError
from localities.models import Locality
from localities.utils import parse_bbox
from localities.map_clustering import cluster


class Command(BaseCommand):
    args = '<icon_width> <icon_height>'
    help = 'Generate locality cluster cache'
    MAX_ZOOM = 18

    option_list = BaseCommand.option_list + (
        make_option(
            '--tabs', action='store_true', dest='use_tabs', default=False,
            help='Use when input file is tab delimited'
        ),
    )

    def handle(self, *args, **options):

        if len(args) != 2:
            raise CommandError('Missing required arguments')

        try:
            icon_size = [int(size) for size in args[0:2]]
        except Exception as e:
            raise CommandError(str(e))

        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise CommandError('Icon sizes should be positive numbers')

        localities = Locality.objects.all()
        # localities = Locality.objects.in_bbox(
        #     parse_bbox('4.4558626413345337,6.5171178387202984,4.4624984264373779,6.5220158579049112'))
        loc_clusters = cluster(localities, self.MAX_ZOOM, icon_size[0], icon_size[1], True)
        number = len(loc_clusters)
        index = 1;
        for loc_cluster in loc_clusters:
            print "----------------------------------"
            print "%s/%s count : %s" % (index, number, loc_cluster['count'])
            if loc_cluster['count'] > 1:
                loc_cluster['localities'].sort(key=extract_time, reverse=False)
                master = loc_cluster['localities'].pop(0)
                print "master : %s " % master['uuid']
                try:
                    locality_master = Locality.objects.get(id=master['id'])
                    locality_master.master = None
                    locality_master.save()

                    synonyms = []
                    for synonym in loc_cluster['localities']:
                        # set master of synonym
                        try:
                            locality = Locality.objects.get(id=synonym['id'])
                            if not locality.master:
                                locality.master = locality_master
                                locality.save()
                            synonyms.append(str(synonym['uuid']))
                        except Exception as e:
                            print e
                    print 'synonyms : '+', '.join(synonyms)
                except Exception as e:
                    print e
