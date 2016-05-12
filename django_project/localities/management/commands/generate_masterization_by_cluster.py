# -*- coding: utf-8 -*-
from optparse import make_option

from core.utilities import extract_time
from django.core.management.base import BaseCommand, CommandError
from localities.models import Changeset, Locality, UnconfirmedSynonym
from localities.map_clustering import cluster
from django.contrib.auth.models import User


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

        # get user that responsibility to change this
        user = None
        try:
            user = User.objects.get(username="sharehealthdata")
        except User.DoesNotExist:
            try:
                user = User.objects.get(username="admin")
            except User.DoesNotExist:
                pass

        localities = Locality.objects.all()
        loc_clusters = cluster(localities, self.MAX_ZOOM, icon_size[0], icon_size[1], True)
        number = len(loc_clusters)
        index = 1;
        for loc_cluster in loc_clusters:
            print "%s/%s count : %s" % (index, number, loc_cluster['count'])
            index += 1
            if loc_cluster['count'] > 1:
                for potential_master in loc_cluster['localities']:
                    for potential_synonym in loc_cluster['localities']:
                        print potential_master, potential_synonym
                        if potential_master != potential_synonym:
                            try:
                                UnconfirmedSynonym.objects.get(
                                    locality=potential_master, synonym=potential_synonym)
                            except UnconfirmedSynonym.DoesNotExist:
                                UnconfirmedSynonym(locality=potential_master,
                                                   synonym=potential_synonym).save()
