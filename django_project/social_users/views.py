# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from braces.views import LoginRequiredMixin

from localities.utils import extract_updates
from social_users.models import Profile
from social_users.utils import get_profile, user_updates

LOG = logging.getLogger(__name__)


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

        user = get_object_or_404(User, username=kwargs['username'])
        user = get_profile(user)
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
    url = None
    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
    # get old user
    if kwargs['is_new']:
        if 'username' in kwargs['details']:
            new_username = kwargs['details']['username']
            new_username = new_username.replace(' ', '')
            if user.username != new_username:
                try:
                    old_username = user.username
                    user = User.objects.get(username=new_username)
                    User.objects.get(username=old_username).delete()
                except User.DoesNotExist:
                    pass
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
    if url:
        profile.profile_picture = url
    profile.save()
    return {'user': user}


class GetUserUpdates(View):

    def get(self, request):
        date = request.GET.get('date')
        user = request.GET.get('user')
        if not date:
            date = datetime.now()
        user = get_object_or_404(User, username=user)
        last_updates = user_updates(user, date)
        updates = extract_updates(last_updates)
        result = {}
        result['last_update'] = updates
        result = json.dumps(result, cls=DjangoJSONEncoder)

        return HttpResponse(result, content_type='application/json')
