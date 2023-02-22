# -*- coding: utf-8 -*-
import logging
import json
import os
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from braces.views import FormMessagesMixin, LoginRequiredMixin
from envelope.views import ContactView as EnvelopeContactView
from api.api_views.v2.schema import Schema
from localities.models import Country, DataLoaderPermission
from frontend.forms import DataLoaderForm
from social_users.utils import get_profile

LOG = logging.getLogger(__name__)


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['debug'] = settings.DEBUG
        context['map_max_zoom'] = settings.MAX_ZOOM
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                context['uploader'] = True
            else:
                permission = DataLoaderPermission.objects.filter(
                    uploader=self.request.user)
                if len(permission) <= 0:
                    context['uploader'] = False
                else:
                    context['uploader'] = True
        else:
            context['uploader'] = False
        return context


class MessagesContactView(FormMessagesMixin, EnvelopeContactView):
    form_invalid_message = 'There was en error in the contact form.'
    form_valid_message = 'Thank you for your message.'
    template_name = 'envelope/contact.html'

    def get_context_data(self, **kwargs):
        context = super(MessagesContactView, self).get_context_data(**kwargs)
        context['CHAPCHA_SITE_KEY'] = settings.CHAPCHA_SITE_KEY
        return context

    def form_valid(self, form):
        captcha_response = self.request.POST.get('captcha_response', None)
        if not captcha_response:
            form.add_error(None, "Captcha is invalid")
            return self.form_invalid(form)
        else:
            # lets check the response
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': settings.CHAPCHA_SECRET_KEY,
                'response': captcha_response
            })
            if response.status_code != 200:
                form.add_error(None, "Captcha is invalid")
                return self.form_invalid(form)
            else:
                text = json.loads(response.text)
                if not text['success']:
                    form.add_error(None, "Captcha : " + ','.join(text['error-codes']))
                    return self.form_invalid(form)

        return super(MessagesContactView, self).form_valid(form)


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        context = super(MapView, self).get_context_data(**kwargs)
        context['debug'] = settings.DEBUG
        context['osm_API'] = settings.OSM_API_URL
        context['map_max_zoom'] = settings.MAX_ZOOM
        context['schema'] = json.dumps(Schema().get_schema())
        context['countries'] = Country.objects.order_by('name').values('name', 'parent__name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user)
            self.request.user = get_profile(user, self.request)
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class HelpView(TemplateView):
    template_name = 'help.html'


class AttributionsView(TemplateView):
    template_name = 'attributions.html'


class DonateView(TemplateView):
    template_name = 'donate.html'


class GatherEnrollmentView(TemplateView):
    template_name = 'how_to_gather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DataLoaderView(LoginRequiredMixin, FormView):
    """Handles DataLoader.
    """
    form_class = DataLoaderForm
    template_name = 'dataloaderform.html'

    def get_form_kwargs(self):
        """
        This method is what injects forms with their keyword arguments.
        """
        # grab the current set of form #kwargs
        kwargs = super(DataLoaderView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        # delete old import progress before processing the data
        pathname = os.path.join(
            settings.CACHE_DIR, 'csv-import-progress')
        progress_file = os.path.join(
            pathname, '{}.txt'.format(request.user.username))
        if os.path.exists(progress_file):
            os.remove(progress_file)

        form = DataLoaderForm(
            request.POST, files=request.FILES, user=request.user)

        if form.is_valid():
            form.save(True)

            response = {}
            success_message = 'You have successfully upload your data.'

            response['message'] = success_message
            response['success'] = True
            response['detailed_message'] = (
                'Please wait for Healthsites to validate and load your data. '
                'The status of all your data will be reported here once the '
                'process has been finished. We will also send you an email if '
                'we have finished processing your data.'
            )
            return HttpResponse(json.dumps(
                response,
                ensure_ascii=False),
                content_type='application/javascript')
        else:
            error_message = form.errors
            response = {
                'detailed_message': str(error_message),
                'success': False,
                'message': 'You have failed to load data.'
            }
            return HttpResponse(json.dumps(
                response,
                ensure_ascii=False),
                content_type='application/javascript')
