# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout as auth_logout
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from social_users.models import UserDetail


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfilePage, self).get_context_data(*args, **kwargs)
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

        user = get_object_or_404(User, username=kwargs["username"])
        profile_picture = ""
        shared_links = []
        # check if the user has profile_picture
        # if not, just send empty string
        try:
            user_detail = UserDetail.objects.get(user=user)
            profile_picture = user_detail.profile_picture
            # links = user_detail.link
            # if links is not None:
            #     for item in links:
            #         shared_links.append(item.link)
        except UserDetail.DoesNotExist:
            profile_picture = ""

        user.profile_picture = profile_picture
        user.shared_links = shared_links
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        context['user'] = user
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
