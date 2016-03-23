# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import LocalityAPI, LocalitiesAPI, LocalitySearchAPI, LocalityCreateAPI, LoginAPI

urlpatterns = patterns(
    '',
    url(
		r'^v1/healthsites/facility/details',
		LocalityAPI.as_view(),
		name='api_locality_detail'
	),
	url(
		r'^v1/healthsites/facilities',
		LocalitiesAPI.as_view(),
		name='api_localities'
	),
	url(
		r'^v1/healthsites/search',
		LocalitySearchAPI.as_view(),
		name='api_search_localities'
	),
	url(
		r'^v1/healthsites/facility/add',
		LocalityCreateAPI.as_view(),
		name='api_search_localities'
	),
	url(
		r'^v1/healthsites/login/(?P<social>.*)',
		LoginAPI.as_view(),
		name='api_login'
	)
)
