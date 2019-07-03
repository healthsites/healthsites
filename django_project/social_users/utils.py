# -*- coding: utf-8 -*-

from social_users.models import TrustedUser

from .models import Profile


def get_profile(user, request=None):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
    except Profile.DoesNotExist:
        profile_picture = ''

    user.profile_picture = profile_picture
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
        uid = user.social_auth.get(provider='twitter').uid
        user.social.append({'provider': 'twitter', 'uid': user.username})
    except Exception as e:  # noqa
        pass

    try:
        uid = user.social_auth.get(provider='openstreetmap').uid
        user.social.append({'provider': 'openstreetmap', 'uid': uid})
    except Exception as e:  # noqa
        pass

    # GET SOCIAL AUTH
    user.provider = ''
    if request:
        try:
            social_auth = request.session['social_auth']
            user.profile_picture = social_auth['profile_picture']
            user.provider = social_auth['provider']
        except KeyError:
            pass
    return user
