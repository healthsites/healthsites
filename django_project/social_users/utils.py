__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/03/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from .models import Profile
from social_users.models import TrustedUser


def get_profile(user):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    username = user.username
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
        if user_detail.screen_name != "":
            username = user_detail.screen_name
    except Profile.DoesNotExist:
        profile_picture = ""

    user.profile_picture = profile_picture
    user.screen_name = username
    user.shared_links = shared_links
    try:
        trusted_user = TrustedUser.objects.get(user=user)
        user.is_trusted_user = True
        user.organization = [{"name": org.name, "website": org.clean_website()} for org in
                             trusted_user.organizations.all()]
    except TrustedUser.DoesNotExist:
        user.is_trusted_user = False
    return user
