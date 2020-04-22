# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.documentation import include_docs_urls

from api.api_views.v2.import_progress import ImportCSVProgress
from api.api_views.v2.schema import SchemaView
from .views.api_view import Docs
from .views.facilities import FacilitiesApiView
from .views.locality_create import LocalityCreateApiView
from .views.locality_detail import LocalityDetailApiView
from .views.locality_search import LocalitySearchApiView
from .views.locality_synonym import LocalitySynonymApiView

# API Version 2
from api.api_views.v2.countries.search import Autocomplete as CountryAutocomplete
from api.api_views.v2.facilities.cluster import GetCluster
from api.api_views.v2.facilities.detail import (
    GetDetailFacility, GetDetailFacilityByUUID)
from api.api_views.v2.facilities.list import (
    BulkUpload, GetFacilities, GetFacilitiesCount, GetFacilitiesStatistic)
from api.api_views.v2.facilities.shapefile import GetShapefileDetail, GetShapefileDownload
from api.api_views.v2.facilities.search import Autocomplete
from api.api_views.v2.googlemaps.search import SearchByGeoname
from api.api_views.v2.gather_enrollment import GatherEnrollment
from api.api_views.v2.get_migration_progress import GetMigrationProgress
from api.api_views.v2.users.changesets import GetChangesets
from api.api_views.v2.pending.list import GetPendingReviews, GetPendingUpdates
from api.api_views.v2.pending.detail import GetDetailPendingReviews

countries_api = patterns(
    '',
    url(r'^autocomplete',
        CountryAutocomplete.as_view())
)
facilities_api = patterns(
    '',
    url(r'^shapefile/(?P<country>.+)/detail',
        GetShapefileDetail.as_view()),
    url(r'^shapefile/(?P<country>.+)/download',
        GetShapefileDownload.as_view()),

    url(r'^cluster', GetCluster.as_view()),
    url(r'^count',
        GetFacilitiesCount.as_view()),
    url(r'^statistic',
        GetFacilitiesStatistic.as_view()),
    url(r'^autocomplete/',
        Autocomplete.as_view()),
    url(r'^bulk/create', BulkUpload.as_view()),
    url(r'^(?P<osm_type>\w+)/(?P<osm_id>-?\d+)',
        GetDetailFacility.as_view()),
    url(r'by-uuid/(?P<uuid>[\w\-]+)',
        GetDetailFacilityByUUID.as_view()),
    url(r'^',
        GetFacilities.as_view()),
)
gmaps_api = patterns(
    '',
    url(r'^search/geoname',
        SearchByGeoname.as_view())
)
user_api = patterns(
    '',
    url(r'^changesets',
        GetChangesets.as_view()),
    url(r'^reviews',
        GetPendingReviews.as_view()),
    url(r'^updates',
        GetPendingUpdates.as_view()),
)
pending_api = patterns(
    '',
    url(r'reviews/(?P<id>-?\d+)',
        GetDetailPendingReviews.as_view()),
)
gather_api = patterns(
    '',
    url(r'enrollment/',
        GatherEnrollment.as_view(), name='api_gather_enrollment'),
)
api_v2 = patterns(
    '',
    url(r'countries/', include(countries_api)),
    url(r'facilities/', include(facilities_api)),
    url(r'gmaps/', include(gmaps_api)),
    url(r'gather/', include(gather_api)),
    url(r'pending/', include(pending_api)),
    url(r'user/(?P<username>.*)/', include(user_api)),
    url(r'migration-progress/',
        GetMigrationProgress.as_view(), name='api_get_migration_progress'),
    url(r'csv-import-progress/',
        ImportCSVProgress.as_view(), name='api_get_csv_import_progress')
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
