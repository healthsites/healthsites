# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class LocalityCreateApiView(View):
    def _parse_request_params(self, request):
        if not (all(param in request.GET for param in ['geom'])):
            raise Http404
        return request.GET['geom']

    def get(self, request, *args, **kwargs):
        geom = self._parse_request_params(request)
        request.session['new_geom'] = geom
        map_url = reverse('map')
        return HttpResponseRedirect(map_url)
