# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

import logging

from django.contrib.gis.db import models
from django.contrib.gis.db.models import QuerySet
from django.db.models import Q

LOG = logging.getLogger(__name__)


class OSMQuerySet(QuerySet):
    def in_bbox(self, bbox):
        """
        Filter Localities within a bbox
        """
        return self.filter(geometry__bboverlaps=bbox)

    def in_polygon(self, polygon):
        """
        Filter Localities within a polygon
        """
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
                    query |= Q(**{'{}__icontains'.format(key): x})
                queryset = queryset.filter(query)
        return queryset


class OSMManager(models.Manager):
    def get_queryset(self):
        return OSMQuerySet(self.model, using=self._db)
