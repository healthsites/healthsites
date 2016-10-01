# -*- coding: utf-8 -*-
import logging
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from model_utils.managers import PassThroughManagerMixin

LOG = logging.getLogger(__name__)


class PassThroughGeoManager(PassThroughManagerMixin, models.GeoManager):
    """
    https://django-model-utils.readthedocs.org/en/latest/managers.html#mixins
    """

    pass


class LocalitiesQuerySet(GeoQuerySet):
    def in_bbox(self, bbox):
        """
        Filter Localities within a bbox
        """

        LOG.debug('Filtering Localities using bbox: %s', bbox.wkt)
        return self.filter(geom__contained=bbox)

    def get_lnglat(self):
        """
        Use database to extract geometry

        Creating Python objects is expensive :)
        """

        return self.extra(select={'lnglat': 'st_x(geom)||$$,$$||st_y(geom)'})

    def in_polygon(self, polygon):
        """
        Filter Localities within a polygon
        """

        LOG.debug('Filtering Localities using polygon: %s', polygon)
        return self.filter(geom__within=polygon)
