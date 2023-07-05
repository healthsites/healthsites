"""Factory for User."""
import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserF(factory.django.DjangoModelFactory):
    """Factory for User."""

    username = factory.Sequence(lambda n: 'user_{}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:  # noqa: D106
        model = User


def create_user(role: str, **kwargs):
    """Create user with role."""
    user = UserF(**kwargs)
    user.profile.role = role
    user.profile.save()
    return user
