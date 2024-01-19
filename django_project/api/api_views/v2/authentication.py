__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

from rest_framework import authentication, exceptions

from api.models.user_api_key import UserApiKey, ApiKeyAccess
from core.models.preferences import SitePreferences


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        preference = SitePreferences.preferences()
        api_key = request.GET.get('api-key', None)
        if not api_key:
            raise exceptions.AuthenticationFailed('API key is needed')
        key = UserApiKey.get_key_from_api_key(api_key)
        site_url_msg = f' at {preference.site_url}' if preference.site_url else ''
        if not key:
            raise exceptions.AuthenticationFailed(
                'API key invalid. '
                'Please recreate your key using the enrollment '
                f'form on your profile page{site_url_msg}.'
            )
        if not key.is_active:
            raise exceptions.AuthenticationFailed(
                'This API key is not active. '
                'Please wait for it to be approved by the admins.'
            )
        user = key.user
        if not user:
            raise exceptions.AuthenticationFailed(
                'API key invalid. '
                'Please recreate your key using the enrollment '
                f'form on your profile page {site_url_msg}.'
            )
        if request.method != 'GET' and not key.allow_write:
            raise exceptions.AuthenticationFailed(
                'This API key does not include access permissions to post data.'
                f'Please ask the admins{site_url_msg} '
                f'if you need POST permissions.'
            )
        allow = ApiKeyAccess.request(
            key, request.build_absolute_uri(), request.method
        )
        if not allow:
            raise exceptions.AuthenticationFailed(
                "The number of today API requests is too high. "
                f"The limit is {key.limit} per day. "
                "Please ask admin to increase the limit. "
            )

        return (user, None)
