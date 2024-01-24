"""Contains singleton model."""

from django.db import models


class SingletonModel(models.Model):
    """Singleton Abstract Model that just have 1 data on database."""

    class Meta:  # noqa: D106
        abstract = True

    def save(self, *args, **kwargs):
        """Save model."""
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete model."""
        pass

    @classmethod
    def load(cls):
        """Load the singleton model with 1 object."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
