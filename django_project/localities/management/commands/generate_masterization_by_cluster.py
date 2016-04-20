# -*- coding: utf-8 -*-
from optparse import make_option

from core.utilities import extract_time
from django.core.management.base import BaseCommand, CommandError
from localities.models import Changeset, Locality
from localities.utils import parse_bbox
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
        # localities = Locality.objects.in_bbox(parse_bbox('107.14000000,-6.839783821352297,107.14100000,-6.80000000'))
        loc_clusters = cluster(localities, self.MAX_ZOOM, icon_size[0], icon_size[1], True)
        number = len(loc_clusters)
        index = 1;
        for loc_cluster in loc_clusters:
            print "%s/%s count : %s" % (index, number, loc_cluster['count'])
            index += 1
            if loc_cluster['count'] > 1:
                loc_cluster['localities'].sort(key=extract_time, reverse=True)
                # check_master
                master = None
                index = 0
                for locality in loc_cluster['localities']:
                    checked_loc = Locality.objects.get(id=locality['id'])
                    if "raw_source" in checked_loc.repr_dict()['values']:
                        master = loc_cluster['localities'].pop(index)
                        break
                    index += 1
                if not master:
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
                            locality.master = locality_master
                            locality.save()
                            synonyms.append(str(synonym['uuid']))

                            # fill the existed value
                            synonym_value = locality.repr_dict()['values']
                            master_value = locality_master.repr_dict()['values']

                            new_values = {}
                            for key in synonym_value.keys():
                                if not key in master_value:
                                    # fill that value if not in master dict
                                    new_values[key] = synonym_value[key]
                                elif master_value[key].replace("-", "").replace("|", "") == "":
                                    # fill that value if the value in master is filled with just "|" or "-" or both
                                    new_values[key] = synonym_value[key]

                            if new_values and User:
                                # there are some changes so create a new changeset
                                tmp_changeset = Changeset.objects.create(social_user=user)
                                locality_master.changeset = tmp_changeset
                                locality_master.set_values(new_values, user, tmp_changeset)
                                locality_master.save()

                        except Exception as e:
                            print e
                    print 'synonyms : ' + ', '.join(synonyms)
                except Exception as e:
                    print e
