from .models import Profile
from social_users.models import TrustedUser

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/03/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def get_profile(user):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
    except Profile.DoesNotExist:
        profile_picture = ""

    user.profile_picture = profile_picture
    user.screen_name = user.username
    user.shared_links = shared_links
    try:
        trusted_user = TrustedUser.objects.get(user=user)
        user.is_trusted_user = True
        user.organisations = [{"name": org.name, "website": org.clean_website()} for org in
                              trusted_user.organisations_supported.all().filter(organisationsupported__is_staff=True)]
        user.organisations_supported = [{"name": org.name, "website": org.clean_website()} for org in
                                        trusted_user.organisations_supported.all().filter(
                                            organisationsupported__is_staff=False)]
    except TrustedUser.DoesNotExist:
        user.is_trusted_user = False

    # GETTING SOCIAL LINK
    user.social = []
    try:
        uid = user.social_auth.get(provider='twitter').uid
        user.social.append({"provider": "twitter", "uid": user.username})
    except Exception:
        pass

    try:
        uid = user.social_auth.get(provider='facebook').uid
        user.social.append({"provider": "facebook", "uid": uid})
    except Exception:
        pass
    return user
