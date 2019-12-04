# -*- coding: utf-8 -*-
from envelope.views import ContactView
from django.conf.urls import patterns, url
from braces.views import FormMessagesMixin
from .views import AboutView, AttributionsView, HelpView, MainView, \
    GatherEnrollmentView, DonateView
from .flatpages import views


class MessagesContactView(FormMessagesMixin, ContactView):
    form_invalid_message = 'There was en error in the contact form.'
    form_valid_message = 'Thank you for your message.'
    template_name = 'envelope/contact.html'


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
