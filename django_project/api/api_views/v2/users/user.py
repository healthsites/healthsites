from rest_framework.views import Response

from api.api_views.v2.base_api import BaseAPIWithAuthAndApiKey
from api.api_views.v2.schema import ApiSchemaBase
from social_users.serializer.user import UserSerializer


class UserProfile(BaseAPIWithAuthAndApiKey):
    """Return logged in user detail."""
    filter_backends = (ApiSchemaBase,)
    api_label = {
        'GET': 'read'
    }

    def get(self, request):
        return Response(UserSerializer(self.request.user).data)
