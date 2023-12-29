from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models.user_api_key import UserApiKey, ApiKeyEnrollment


class UserApiKeySerializer(ModelSerializer):
    class Meta:
        model = UserApiKey
        exclude = ()


class ApiKeyEnrollmentSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj: ApiKeyEnrollment):
        """Return username."""
        return obj.username

    class Meta:
        model = ApiKeyEnrollment
        exclude = ()
