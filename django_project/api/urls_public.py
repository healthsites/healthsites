"""Version 3 API"""
from django.conf.urls import include, url

from api.api_views.v2.countries.search import (
    Autocomplete as CountryAutocomplete
)
from api.api_views.v2.facilities import (
    Autocomplete,
    GetDetailFacility, GetDetailFacilityByUUID,
    GetCluster, GetFacilitiesCount, GetFacilitiesStatistic,
    GetShapefileDetail, GetShapefileDownload,
    GetFacilities
)
from api.api_views.v2.googlemaps.search import SearchByGeoname
from api.api_views.v2.import_progress import ImportCSVProgress
from api.api_views.v2.pending.list import GetPendingReviews, GetPendingUpdates
from api.api_views.v2.users.changesets import GetChangesets

countries_api = [
    url(r'^autocomplete', CountryAutocomplete.as_view())
]

# facilities API
facilities_api = [
    url(r'^(?P<osm_type>\w+)/(?P<osm_id>-?\d+)',
        GetDetailFacility.as_view()),
    url(r'^autocomplete/', Autocomplete.as_view()),
    url(r'by-uuid/(?P<uuid>[\w\-]+)', GetDetailFacilityByUUID.as_view()),
    url(r'^cluster', GetCluster.as_view(), name='get-cluster'),
    url(r'^count', GetFacilitiesCount.as_view(), name='get-count'),
    url(r'^statistic',
        GetFacilitiesStatistic.as_view(), name='get-statistic'),

    url(r'^shapefile/(?P<country>.+)/detail',
        GetShapefileDetail.as_view()),
    url(r'^shapefile/(?P<country>.+)/download',
        GetShapefileDownload.as_view()),
    url(r'^', GetFacilities.as_view(), name='facilities'),
]

# gmaps api
gmaps_api = [
    url(r'^search/geoname',
        SearchByGeoname.as_view(), name='search-geonome')
]

# API about user
user_api = [
    url(r'^changesets',
        GetChangesets.as_view()),
    url(r'^reviews',
        GetPendingReviews.as_view()),
    url(r'^updates',
        GetPendingUpdates.as_view()),
]
urlpatterns = [
    url(r'countries/', include(countries_api)),
    url(r'facilities/', include(facilities_api)),
    url(r'gmaps/', include(gmaps_api)),
    url(r'user/(?P<username>.*)/', include(user_api)),
    url(r'csv-import-progress/',
        ImportCSVProgress.as_view(), name='api_get_csv_import_progress'),
]
