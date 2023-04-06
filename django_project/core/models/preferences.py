"""Model for Website Preferences."""
from django.db import models

from core.models.singleton import SingletonModel


class SitePreferences(SingletonModel):
    """Preference settings specifically for website.
    """

    default_max_request_api = models.IntegerField(
        default=50,
        help_text='Default max request per day for api key.'
    )

    class Meta:  # noqa: D106
        verbose_name_plural = "site preferences"

    @staticmethod
    def preferences() -> "SitePreferences":
        """Load Site Preference."""
        return SitePreferences.load()

    def __str__(self):
        return 'Site Preference'
