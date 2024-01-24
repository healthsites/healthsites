"""Site preference serializer."""

from rest_framework import serializers

from core.models.preferences import SitePreferences


class SitePreferencesSerializer(serializers.ModelSerializer):
    """Site preference serializer."""

    class Meta:  # noqa: D106
        model = SitePreferences
        exclude = ()
