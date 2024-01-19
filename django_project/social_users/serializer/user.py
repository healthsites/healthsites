"""Site preference serializer."""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:  # noqa: D106
        model = User
        exclude = ('id', 'password', 'user_permissions', 'groups')
