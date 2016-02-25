# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import MainView, AboutView, HelpView
from envelope.views import ContactView
from braces.views import FormMessagesMixin


class MessagesContactView(FormMessagesMixin, ContactView):
    form_invalid_message = "There was en error in the contact form."
    form_valid_message = "Thank you for your message."
    template_name = "envelope/contact.html"


urlpatterns = patterns(
        '',
        # basic app views
        url(r'^$', MainView.as_view(), name='home'),
        url(r'^contact/', MessagesContactView.as_view(), name='envelope-contact'),
        url(r'^about$', AboutView.as_view(), name='about'),
        url(r'^help', HelpView.as_view(), name='help'),
        url(r'^map$', 'frontend.views.map', name='map'),
)
