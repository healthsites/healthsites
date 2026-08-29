from drf_spectacular.utils import extend_schema
from rest_framework.views import Response

from api.api_views.v2.base_api import BaseAPIWithAuthAndApiKey
from api.api_views.v2.schema import ApiSchemaBase
from social_users.serializer.user import UserSerializer


class UserProfile(BaseAPIWithAuthAndApiKey):
    """User profile endpoint."""

    filter_backends = (ApiSchemaBase,)
    api_label = {
        'GET': 'read'
    }

    @extend_schema(
        summary='Get user profile',
        description='Returns the profile of the currently authenticated user.',
    )
    def get(self, request):
        return Response(UserSerializer(self.request.user).data)
