# -*- coding: utf-8 -*-
import json
import requests
from envelope.views import ContactView
from django.conf import settings
from django.conf.urls import patterns, url
from braces.views import FormMessagesMixin
from .views import AboutView, AttributionsView, HelpView, MainView, \
    GatherEnrollmentView, DonateView
from .flatpages import views


class MessagesContactView(FormMessagesMixin, ContactView):
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


urlpatterns = patterns(
    '',
    # basic app views
    url(r'^$', MainView.as_view(), name='home'),
    url(r'^how-to-gather', GatherEnrollmentView.as_view(),
        name='how-to-gather'),
    url(r'^contact/', MessagesContactView.as_view(), name='envelope-contact'),
    url(r'^about$', AboutView.as_view(), name='about'),
    url(r'^help', HelpView.as_view(), name='help'),
    url(r'^map$', 'frontend.views.map', name='map'),
    url(r'^attributions$', AttributionsView.as_view(), name='attribution'),
    url(r'^donate$', DonateView.as_view(), name='donate'),
    url(r'^campaign/(?P<url>.*/)$', views.flatpage),

)
