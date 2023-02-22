__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.auth.models import User
from social_users.models import Profile


def save_profile(backend, user, response, *args, **kwargs):
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

    profile_picture = None
    if backend.name == 'facebook':
        profile_picture = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    elif backend.name == 'twitter':
        profile_picture = response.get('profile_image_url', '').replace('_normal', '')
    elif backend.name == 'google-oauth2':
        profile_picture = response['image'].get('url')
    elif backend.name == 'openstreetmap':
        profile_picture = response['avatar']

    profile, created = Profile.objects.get_or_create(user=user)
    if profile_picture:
        profile.profile_picture = profile_picture
    profile.save()

    kwargs['request'].session['social_auth'] = {
        'profile_picture': profile_picture,
        'provider': backend.name
    }

    return {'user': user}
