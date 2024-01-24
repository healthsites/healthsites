"""Version 3 API"""
from django.conf.urls import include, url

from api.api_views.v2.facilities import (
    GetFacilities, GetDetailFacilityV3, GetShapefileDownloadV3,
    GetFacilitiesStatisticV3
)
from api.api_views.v2.users.user import UserProfile

facilities_api = [
    url(r'^(?P<osm_type>\w+)/(?P<osm_id>-?\d+)',
        GetDetailFacilityV3.as_view()),
    url(r'^statistic/', GetFacilitiesStatisticV3.as_view(),
        name='facilities-statistic-v3'),
    url(r'^', GetFacilities.as_view(), name='facilities-v3'),
]
shapefile_api = [
    url(r'^(?P<country>.+)',
        GetShapefileDownloadV3.as_view(),
        name='shpefile-download-v3'
        )
]

urlpatterns = [
    url(r'facilities/', include(facilities_api)),
    url(r'shapefile/', include(shapefile_api)),
    url(r'user/', UserProfile.as_view(), name='user-detail'),
]
