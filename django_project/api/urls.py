# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.facilities import FacilitiesApiView
from .views.locality_create import LocalityCreateApiView
from .views.locality_detail import LocalityDetailApiView
from .views.locality_synonym import LocalitySynonymApiView
from .views.locality_search import LocalitySearchApiView

urlpatterns = patterns(
    '',
    url(r'^v1/healthsites/facilities', FacilitiesApiView.as_view(), name='api_facilities'),
    url(r'^v1/healthsites/search', LocalitySearchApiView.as_view(), name='api_search_localities'),
    url(r'^v1/healthsites/facility/details', LocalityDetailApiView.as_view(), name='api_locality_detail'),
    url(r'^v1/healthsites/synonyms', LocalitySynonymApiView.as_view(), name='api_locality_synonyms'),
    url(r'^v1/healthsites/facility/add', LocalityCreateApiView.as_view(), name='api_search_localities'),
)
