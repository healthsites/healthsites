__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '24/02/23'

import logging

from braces.views import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView

from api.forms import EnrollmentForm

LOG = logging.getLogger(__name__)


class EnrollmentFormView(LoginRequiredMixin, CreateView):
    """Handles EnrollmentForm."""

    form_class = EnrollmentForm
    template_name = 'enrollment_form.html'
    success_url = ''

    def form_valid(self, form):
        response = super(EnrollmentFormView, self).form_valid(form)
        self.object.generate_api_key(self.request.user)
        return response

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
