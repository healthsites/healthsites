# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

# API Version 2
from localities_healthsites_osm.api_views.osm.facilities.detail import (
    GetDetailFacility
)
from localities_healthsites_osm.api_views.osm.facilities.list import GetFacilities

api_osm = patterns(
    '',
    url(r'^docs/', include_docs_urls(title='Healthsites API OSM')),
    url(r'^schema/', get_schema_view(title='Healthsites API OSM')),
    url(r'^facilities/(?P<uuid>[\w\+%_& ]+)',
        GetDetailFacility.as_view(), name='api_osm_facility_detail'),
    url(r'^facilities',
        GetFacilities.as_view(), name='api_osm_facility_list'),
)
