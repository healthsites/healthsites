from rest_framework.serializers import ModelSerializer

from api.models.user_api_key import UserApiKey


class UserApiKeySerializer(ModelSerializer):
    class Meta:
        model = UserApiKey
        exclude = ()
