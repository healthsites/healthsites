# -*- coding: utf-8 -*-

from django.forms import models

from api.models.user_api_key import ApiKeyEnrollment


class EnrollmentForm(models.ModelForm):
    """Form for Enrollment. """

    class Meta:
        model = ApiKeyEnrollment
        exclude = ('time', 'approved', 'api_key')
