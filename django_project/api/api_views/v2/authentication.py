__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

from rest_framework import authentication, exceptions

from api.models.user_api_key import UserApiKey, ApiKeyAccess


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.GET.get('api-key', None)
        if not api_key:
            raise exceptions.AuthenticationFailed('api-key is needed')
        key = UserApiKey.get_key_from_api_key(api_key)
        if not key:
            raise exceptions.AuthenticationFailed(
                'api-key is invalid, '
                'please recreate using enrollment form on profile page.'
            )
        if not key.is_active:
            raise exceptions.AuthenticationFailed(
                'api-key is not active, please wait for admin approval.'
            )
        user = key.user
        if not user:
            raise exceptions.AuthenticationFailed('api-key is invalid')
        if request.method != 'GET' and not key.allow_write:
            raise exceptions.AuthenticationFailed(
                'This api-key is not allowed to post data. '
                'Please ask admin to update it.'
            )
        allow = ApiKeyAccess.request(key, request.build_absolute_uri())
        if not allow:
            raise exceptions.AuthenticationFailed(
                "The number of today API requests is too high. "
                f"The limit is {key.limit} per day. "
                "Please ask admin to increase limit. "
            )

        return (user, None)
