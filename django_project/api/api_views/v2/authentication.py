__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/01/19'

from django.urls import reverse
from rest_framework import authentication, exceptions

from api.models.user_api_key import UserApiKey, ApiKeyAccess


class APIKeyAuthentication(authentication.BaseAuthentication):
    """DRF authentication backend that validates requests via an API key.

    The key may be supplied as:
    - A query parameter:      ?api-key=<value>
    - An Authorization header: Authorization: Bearer <value>
    """

    def authenticate(self, request):
        """Authenticate the request using an API key.

        The key is read from the 'api-key' query parameter or, if absent,
        from the 'Authorization: Bearer <value>' request header.

        Validates that the key exists, is active, has write access for
        non-GET requests, and has not exceeded its daily request limit.

        Returns a (user, None) tuple on success, or raises AuthenticationFailed.
        """
        profile_page = request.build_absolute_uri(
            reverse('userprofilepage')
        )
        api_key = request.GET.get('api-key', None)
        if not api_key:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                api_key = auth_header[len('Bearer '):]
        if not api_key:
            raise exceptions.AuthenticationFailed(
                'API key is required. '
                'Provide it as a query parameter (?api-key=<value>) '
                'or as a request header (Authorization: Bearer <value>).'
            )
        key = UserApiKey.get_key_from_api_key(api_key)
        if not key:
            raise exceptions.AuthenticationFailed(
                'API key invalid. '
                'Please recreate your key using the enrollment '
                f'form on your profile page: {profile_page}.'
            )
        if not key.is_active:
            raise exceptions.AuthenticationFailed(
                'This API key is inactive. '
                'Please wait for it to be approved by an administrator.'
            )
        user = key.user
        if not user:
            raise exceptions.AuthenticationFailed(
                'API key invalid. '
                'Please recreate your key using the enrollment '
                f'form on your profile page: {profile_page}.'
            )
        if request.method != 'GET' and not key.allow_write:
            raise exceptions.AuthenticationFailed(
                'This API key does not have write access. '
                'Please contact an administrator if you need POST permissions.'
            )
        allow = ApiKeyAccess.request(
            key, request.build_absolute_uri(), request.method
        )
        if not allow:
            raise exceptions.AuthenticationFailed(
                f"Daily request limit of {key.limit} has been reached. "
                "Please contact an administrator to increase your limit."
            )

        return (user, None)
