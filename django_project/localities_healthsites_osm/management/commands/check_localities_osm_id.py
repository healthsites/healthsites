# -*- coding: utf-8 -*-
from django.contrib.gis.measure import Distance
from django.core.management.base import BaseCommand
from localities.models import Locality
from localities.models import Country
from localities_osm.models.locality import (
    LocalityOSMNode,
    LocalityOSMWay
)
from localities_healthsites_osm.models import (
    LocalityHealthsitesOSM
)


class Command(BaseCommand):
    help = 'CHeck osm id of localities'

    def handle(self, *args, **options):
        country = Country.objects.get(
            name="Indonesia"
        )
        localities = Locality.objects.in_polygon(
            country.polygon_geometry)
        total = localities.count()
        for index, locality in enumerate(localities):
            data = locality.repr_dict()
            osm_type = None
            osm_id = None
            accepted = False
            print '%s/%s' % (index, total)
            try:
                # this is obviously from osm
                osm = data['source_url'].split('www.openstreetmap.org/')[1].split('/')
                osm_type = osm[0]
                osm_id = osm[1]
                accepted = True
            except IndexError:
                name = data['name']

                # TODO: Update how to match this locality and osm
                # check by name match
                by_names = LocalityOSMNode.objects.filter(
                    name__iexact=name)
                if by_names.count() == 0:
                    by_names = LocalityOSMWay.objects.filter(
                        name__iexact=name)
                name_match = True if by_names.count() >= 1 else False

                # check by name location
                by_geom = LocalityOSMNode.objects.filter(
                    geometry__distance_lt=(locality.geom, Distance(m=100)))
                if by_geom.count() == 0:
                    by_geom = LocalityOSMWay.objects.filter(
                        geometry__contains=locality.geom)
                geom_match = True if by_geom.count() >= 1 else False

                print '%s : [%s , %s]' % (name, name_match, geom_match)

            if osm_id and osm_type:
                instance, crt = LocalityHealthsitesOSM.objects.get_or_create(
                    healthsite=locality,
                    osm_id=osm_id,
                    osm_type=osm_type
                )
                instance.acceptance = accepted
                instance.save()
