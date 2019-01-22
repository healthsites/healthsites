__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'
from django.conf.urls import patterns, url
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from localities_healthsites_osm.api_views.v2.facilities import (
    GetDetailFacility, GetFacilities)

urlpatterns = patterns(
    '',
    url(r'^docs/', include_docs_urls(title='Healthsites API Version 2')),
    url(r'^schema/', get_schema_view(title='Healthsites API Version 2 Schema')),
    url(r'^facilities/(?P<osm_type>[\w\+%_& ]+)/(?P<osm_id>[\w\+%_& ]+)',
        GetDetailFacility.as_view(), name='api_v2_facility_detail'),
    url(r'^facilities',
        GetFacilities.as_view(), name='api_v2_facility_list'),
)
