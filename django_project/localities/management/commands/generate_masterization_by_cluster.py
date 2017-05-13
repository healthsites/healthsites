# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from localities.map_clustering import cluster
from localities.masterization import report_locality_as_unconfirmed_synonym
from localities.models import Locality


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
        loc_clusters = cluster(localities, self.MAX_ZOOM, icon_size[0], icon_size[1], True)
        number = len(loc_clusters)
        index = 1
        for loc_cluster in loc_clusters:
            print '%s/%s count : %s' % (index, number, loc_cluster['count'])
            index += 1
            if loc_cluster['count'] > 1:
                print loc_cluster['localities']
                for potential_master in loc_cluster['localities']:
                    for potential_synonym in loc_cluster['localities']:
                        if potential_synonym['id'] != potential_master['id']:
                            report_locality_as_unconfirmed_synonym(
                                potential_synonym['id'], potential_master['id']
                            )
