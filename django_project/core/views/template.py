__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/08/21'

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class MapView(TemplateView):
    template_name = 'map.html'
