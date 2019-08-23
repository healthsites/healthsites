# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url

from .views import LogoutUser, ProfilePage, UserProfilePage, UserSigninPage
from localities_osm_extension.views import execute_migration
from social_users.views import ProfileUpdate

urlpatterns = patterns(
    '',
    url('', include('social_django.urls', namespace='social')),
    url(r'^signin/$', UserSigninPage.as_view(), name='usersignpage'),
    url(r'^profile/$', UserProfilePage.as_view(), name='userprofilepage'),
    url(r'^profile-update/$', ProfileUpdate.as_view(), name='userprofileupdate'),
    url(
        r'^profile/(?P<username>.*)/$', ProfilePage.as_view(),
        name='profile'
    ),
    url(
        r'^migrate-data/(?P<username>.*)/$',
        execute_migration,
        name='migrate-user-data'
    ),
    url(r'^logout/$', LogoutUser.as_view(), name='logout_user')
)
