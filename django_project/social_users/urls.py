# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url

from .views import GetUserUpdates, LogoutUser, ProfilePage, UserProfilePage, UserSigninPage

urlpatterns = patterns(
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^signin/$', UserSigninPage.as_view(), name='usersignpage'),
    url(r'^profile/$', UserProfilePage.as_view(), name='userprofilepage'),
    url(
        r'^profile/(?P<username>.*)/$', ProfilePage.as_view(),
        name='profile'
    ),
    url(r'^logout/$', LogoutUser.as_view(), name='logout_user'),
    url(
        r'^user/updates/$', GetUserUpdates.as_view(), name='user-updates'
    ),
)
