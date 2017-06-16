# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User

from social_users.models import Profile

LOG = logging.getLogger(__name__)


def save_profile(backend, user, response, *args, **kwargs):
    # get old user
    if kwargs['is_new']:
        new_username = kwargs['details'].get('username')
        if new_username:
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

    url = profile_picture_url(backend=backend, response=response)
    if url:
        profile.profile_picture = url
    profile.save()
    return {'user': user}


def profile_picture_url(backend, response):
    url = None

    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')

    return url
