# -*- coding: utf-8 -*-
from django.contrib.gis.measure import Distance
from django.core.management.base import BaseCommand
from localities.models import Locality
from localities_osm.models.locality import (
    LocalityOSMView
)
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)


class Command(BaseCommand):
    """
    This command try to making check osm_id from healthsittes locality
    and also on docker osm data.

    """

    help = 'Check osm id of localities'

    def handle(self, *args, **options):
        localities = Locality.objects.all()
        total = localities.count()
        for index, locality in enumerate(localities):
            data = locality.repr_dict()
            osm_type = None
            osm_id = None
            print '%s/%s' % (index, total)
            try:
                # this is obviously from osm
                osm = data['source_url'].split('www.openstreetmap.org/')[1].split('/')
                osm_type = osm[0]
                osm_id = osm[1]
            except (IndexError, KeyError):
                name = data['name']
                # TODO: Update how to match this locality and osm
                # check by name match
                by_names = LocalityOSMView.objects.filter(
                    name__iexact=name)
                name_match = True if by_names.count() >= 1 else False

                # check by name location
                by_geom = LocalityOSMView.objects.filter(
                    geometry__distance_lt=(locality.geom, Distance(m=100)))
                if by_geom.count() == 0:
                    by_geom = LocalityOSMView.objects.filter(
                        geometry__contains=locality.geom)
                geom_match = True if by_geom.count() >= 1 else False

                # if geom match and name match, it is same locality
                if geom_match:
                    osm_id = by_geom[0].osm_id
                    osm_type = by_geom[0].osm_type

                print '%s : [%s , %s]' % (name, name_match, geom_match)

            instance, crt = LocalityHealthsitesOSM.objects.get_or_create(
                osm_id=osm_id,
                osm_type=osm_type,
            )
            instance.save()
