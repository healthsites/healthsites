# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Count, Max, Min

from core.utilities import extract_time
from localities.models import Locality, LocalityArchive
from social_users.models import TrustedUser

from .models import Profile


def get_profile(user):
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
            trusted_user.organisations_supported
            .all()
            .filter(organisationsupported__is_staff=True)
        )

        user.organisations = [
            {'name': org.name, 'website': org.clean_website()} for org in supported_organisations
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
    except Exception:
        pass

    try:
        uid = user.social_auth.get(provider='facebook').uid
        user.social.append({'provider': 'facebook', 'uid': uid})
    except Exception:
        pass
    return user


def user_updates(user, date):
    updates = []
    # from locality archive
    ids = (
        LocalityArchive.objects
        .filter(changeset__social_user=user).filter(changeset__created__lt=date)
        .order_by('-changeset__created')
        .values('changeset', 'object_id')
        .annotate(id=Min('id')).values('id')
    )
    updates_temp = (
        LocalityArchive.objects
        .filter(changeset__social_user=user).filter(changeset__created__lt=date)
        .filter(id__in=ids)
        .order_by('-changeset__created')
        .values('changeset', 'changeset__created', 'changeset__social_user__username', 'version')
        .annotate(edit_count=Count('changeset'), locality_id=Max('object_id'))[:10]
    )
    changesets = []
    for update in updates_temp:
        changesets.append(update['changeset'])
        updates.append(get_update_detail(update))

    # get from locality if not in Locality Archive yet
    updates_temp = (
        Locality.objects
        .filter(changeset__social_user=user).exclude(changeset__in=changesets)
        .order_by('-changeset__created')
        .values('changeset', 'changeset__created', 'changeset__social_user__username', 'version')
        .annotate(edit_count=Count('changeset'), locality_id=Max('id'))[:10]
    )
    for update in updates_temp:
        updates.append(get_update_detail(update))

    updates.sort(key=extract_time, reverse=True)
    return updates[:10]


def get_update_detail(update):
    profile = get_profile(User.objects.get(username=update['changeset__social_user__username']))
    update['nickname'] = profile.screen_name
    update['changeset__created'] = update['changeset__created']
    return update
