# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout as auth_logout
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from social_users.models import Profile


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfilePage, self).get_context_data(*args, **kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()
            ]
        return context

def getProfile(user):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
        username = user_detail.screen_name
    except Profile.DoesNotExist:
        profile_picture = ""

    user.profile_picture = profile_picture
    user.username = username
    user.shared_links = shared_links
    return user


class ProfilePage(TemplateView):
    template_name = 'social_users/profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        user = get_object_or_404(User, username=kwargs["username"])
        user = getProfile(user)
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        context['user'] = user
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


def save_profile(backend, user, response, *args, **kwargs):
    username = ""
    try:
        name = response['screen_name']
        username = name
    except Exception as exept:
        try:
            name = response['first_name']
            username = name
            try:
                name = response['last_name']
                username += name
            except Exception as exept:
                print exept
        except Exception as exept:
            print exept

    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    profile.screen_name = username
    if url:
        profile.profile_picture = url
    profile.save()
