# -*- coding: utf-8 -*-
import logging
import operator

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models import Q

from model_utils.managers import PassThroughManagerMixin

LOG = logging.getLogger(__name__)


class PassThroughGeoManager(PassThroughManagerMixin, models.GeoManager):
    """
    https://django-model-utils.readthedocs.org/en/latest/managers.html#mixins
    """

    pass


class OSMQuerySet(GeoQuerySet):
    def in_bbox(self, bbox):
        """
        Filter Localities within a bbox
        """

        LOG.debug('Filtering Localities using bbox: %s', bbox.wkt)
        return self.filter(geometry__bboverlaps=bbox)

    def in_polygon(self, polygon):
        """
        Filter Localities within a polygon
        """

        LOG.debug('Filtering Localities using polygon: %s', polygon)
        return self.filter(geometry__within=polygon)

    def in_filters(self, filters):
        """
        Filter Localities within the filters input
        """
        queryset = self
        for key, value in filters.items():
            if value:
                query = Q()
                for x in value:
                    query |= Q(**{'{}__contains'.format(key): x})
                queryset = queryset.filter(query)
        LOG.debug('Filtering Localities using filters: %s', filters)
        return queryset
