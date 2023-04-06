"""Schema generator."""

from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas.coreapi import (
    SchemaGenerator, insert_into, LinkNode
)

from api.api_views.v2.authentication import APIKeyAuthentication
from api.api_views.v2.schema import SchemaView

schema_url_patterns = [
    url('api/v3/', include('api.urls_v3')),
]


class CustomSchemaGenerator(SchemaGenerator):

    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()

        paths, view_endpoints = self._get_paths_and_endpoints(request)

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            if APIKeyAuthentication not in view.authentication_classes:
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)

        return links

    def get_schema(self, request=None, public=False):
        return super().get_schema(request, True)


urlpatterns = [
    url(r'^docs/', include_docs_urls(
        title='Healthsites API Version 3',
        description=(
            'To access the api, you need api-key for it.'
        ),
        generator_class=CustomSchemaGenerator,
        patterns=schema_url_patterns,
    )),
    url(r'^schema/', SchemaView.as_view(), name='schema_view'),
]
