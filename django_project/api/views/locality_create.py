# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View


class LocalityCreateApiView(View):
    """ API for creating locality."""

    def _parse_request_params(self, request):
        """ Parse request
        :param request: request
        """
        if not (all(param in request.GET for param in ['geom'])):
            raise Http404
        return request.GET['geom']

    def get(self, request, *args, **kwargs):
        geom = self._parse_request_params(request)
        request.session['new_geom'] = geom
        map_url = reverse('map')
        return HttpResponseRedirect(map_url)
