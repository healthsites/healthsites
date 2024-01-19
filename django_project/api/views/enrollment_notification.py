# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from api.models.user_api_key import ApiKeyEnrollment
from api.serializer.user_api_key import ApiKeyEnrollmentSerializer


class EnrollmentNotificationView(TemplateView):
    template_name = 'emails/api_enrollment_notification.html'

    def get_context_data(self, **kwargs):
        enrollment = get_object_or_404(
            ApiKeyEnrollment, pk=kwargs['pk']
        )
        return ApiKeyEnrollmentSerializer(enrollment).data
