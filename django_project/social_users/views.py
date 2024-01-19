# -*- coding: utf-8 -*-
import logging

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import TemplateView, View
from rest_framework.views import APIView

from api.models.user_api_key import UserApiKey
from api.serializer.user_api_key import UserApiKeySerializer
from social_users.models import Organisation
from social_users.utils import get_profile

LOG = logging.getLogger(__name__)


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()
        ]
        return context


class ProfilePage(TemplateView):
    template_name = 'social_users/profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        context = super().get_context_data(**kwargs)
        context['api_keys'] = None
        try:
            user = User.objects.get(username=kwargs['username'])
            user = get_profile(user, self.request)
            osm_user = False

            # returns API Keys if the profile is it's own user
            if self.request.user == user:
                context['api_keys'] = UserApiKeySerializer(
                    UserApiKey.objects.filter(user=self.request.user),
                    many=True
                ).data
        except User.DoesNotExist:
            user = {
                'username': kwargs['username']
            }
            osm_user = True

        context['user'] = user
        context['osm_user'] = osm_user
        context['osm_API'] = settings.OSM_API_URL
        return context


class UserSigninPage(TemplateView):
    """Login Page"""
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    """Logout views"""

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


class ProfileUpdate(APIView):
    """ POST API To update profile of user."""
    exclude_from_schema = True

    def post(self, request, *args):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        data = request.data
        request.user.first_name = data.get('first-name', None)
        request.user.last_name = data.get('last-name', None)
        request.user.email = data.get('email', None)
        request.user.save()

        org_name = data.get('organisation-name', None)
        site_url = data.get('site-url', None)
        if org_name and site_url:
            if site_url:
                site, created = Site.objects.get_or_create(
                    domain=site_url, name=site_url)
                Organisation.objects.get_or_create(
                    name=org_name,
                    site=site
                )

        return HttpResponseRedirect(
            reverse('profile', kwargs={'username': request.user.username})
        )
