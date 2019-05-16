# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.documentation import include_docs_urls

from api.api_views.v2.schema import SchemaView
from .views.api_view import Docs
from .views.facilities import FacilitiesApiView
from .views.locality_create import LocalityCreateApiView
from .views.locality_detail import LocalityDetailApiView
from .views.locality_search import LocalitySearchApiView
from .views.locality_synonym import LocalitySynonymApiView

# API Version 2
from api.api_views.v2.facilities.detail import GetDetailFacility
from api.api_views.v2.facilities.list import (
    GetFacilities, GetFacilitiesCount, GetFacilitiesStatistic)
from api.api_views.v2.facilities.shapefile import GetFacilitiesShapefileProcess
from api.api_views.v2.facilities.search import Autocomplete
from api.api_views.v2.countries.search import Autocomplete as CountryAutocomplete
from api.api_views.v2.get_migration_progress import GetMigrationProgress

facilities_api = patterns(
    '',
    url(r'^count',
        GetFacilitiesCount.as_view()),
    url(r'^statistic',
        GetFacilitiesStatistic.as_view()),
    url(r'^autocomplete/',
        Autocomplete.as_view()),
    url(r'^shapefile/process/(?P<country_name>[\w\+%_& ]+)',
        GetFacilitiesShapefileProcess.as_view()),
    url(r'^(?P<osm_type>\w+)/(?P<osm_id>-?\d+)',
        GetDetailFacility.as_view()),
    url(r'^',
        GetFacilities.as_view())
)
countries_api = patterns(
    '',
    url(r'^autocomplete',
        CountryAutocomplete.as_view())
)
api_v2 = patterns(
    '',
    url(r'facilities/', include(facilities_api)),
    url(r'countries/', include(countries_api)),
    url(r'migration-progress/',
        GetMigrationProgress.as_view(), name='api_get_migration_progress')
)

urlpatterns = patterns(
    '',
    url(r'^docs/', include_docs_urls(title='Healthsites API Version 2')),
    url(r'^schema/', SchemaView.as_view(), name='schema_view'),
    url(r'^v1/healthsites/facilities', FacilitiesApiView.as_view(), name='api_facilities'),
    url(
        r'^v1/healthsites/search', LocalitySearchApiView.as_view(), name='api_search_localities'
    ),
    url(
        r'^v1/healthsites/facility/details', LocalityDetailApiView.as_view(),
        name='api_locality_detail'
    ),
    url(
        r'^v1/healthsites/facility/synonyms', LocalitySynonymApiView.as_view(),
        name='api_locality_synonyms'
    ),
    url(
        r'^v1/healthsites/facility/add', LocalityCreateApiView.as_view(),
        name='api_search_localities'
    ),
    url(r'^v1', Docs.as_view(), name='docs'),
    url(r'v2/', include(api_v2)),
)
