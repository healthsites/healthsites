# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from social_users.models import TrustedUser

from .models import Profile


def get_profile(user, request=None):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    user.screen_name = user.username
    user.shared_links = shared_links
    try:
        trusted_user = TrustedUser.objects.get(user=user)
        user.is_trusted_user = True

        supported_organisations = (
            trusted_user.organisations_supported.all().filter(
                organisationsupported__is_staff=True)
        )

        user.organisations = [
            {'name': org.name,
             'website': org.clean_website()} for org in supported_organisations
        ]
        user.organisations_supported = [
            {'name': org.name, 'website': org.clean_website()}
            for org in trusted_user.organisations_supported.all().filter(
                organisationsupported__is_staff=False)
        ]
    except TrustedUser.DoesNotExist:
        user.is_trusted_user = False

    # GETTING SOCIAL LINK
    user.social = []
    try:
        uid = user.social_auth.get(provider='openstreetmap').uid
        user.social.append({'provider': 'openstreetmap', 'uid': uid})
    except Exception as e:  # noqa
        pass

    # GET SOCIAL AUTH
    profile_picture = ''
    provider = ''

    # get profile picture
    if request and user == request.user:
        try:
            social_auth = request.session['social_auth']
            profile_picture = social_auth['profile_picture']
            provider = social_auth['provider']
        except KeyError:
            pass
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
    except Profile.DoesNotExist:
        pass

    if not profile_picture:
        try:
            profile_picture = user.social_auth.get(provider='openstreetmap').extra_data['avatar']
        except Exception:
            pass

    user.profile_picture = profile_picture
    user.provider = provider

    return user


def get_osm_name(user):
    """ Getting real osm user name from HS user """
    # get osm name from profile
    profile, created = Profile.objects.get_or_create(user=user)
    if profile.osm_name:
        return profile.osm_name
    # get osm name from API
    try:
        id = user.social_auth.get(provider='openstreetmap').extra_data['id']
        url = settings.OSM_API_URL + '/api/0.6/user/%s' % id
        session = requests.Session()
        response = session.get(url)
        if response.status_code == 200:
            username = \
                response.content.split('display_name="')[1].split("\"")[0]
            profile.osm_name = username
            profile.save()
            return profile.osm_name
    except Exception as e:  # noqa
        return None
