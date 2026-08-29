"""Site preference serializer."""

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    is_default_provider = serializers.SerializerMethodField()

    def get_is_default_provider(self, user: User) -> bool:
        """Return provider is default one."""
        try:
            return user.social_auth.get.provider == settings.DEFAULT_PROVIDER
        except AttributeError:
            return False

    class Meta:  # noqa: D106
        model = User
        exclude = ('id', 'password', 'user_permissions', 'groups')
