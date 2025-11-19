"""Behave steps for URL availability checks."""
from __future__ import annotations

from behave import given, then, when

from features.url_utils import collect_testable_urls

SUCCESS_MAX_STATUS = 399


@given('the list of non-parameterized URLs is prepared')
def gather_urls(context):
    if getattr(context, 'url_tracking_initialised', False):
        return
    context.testable_urls = collect_testable_urls()
    assert context.testable_urls, 'No URLs discovered to test.'
    context.remaining_urls = set(context.testable_urls)
    context.url_tracking_initialised = True


@when('I request "{url}"')
def request_url(context, url):
    assert hasattr(context, 'testable_urls'), 'URL list has not been prepared.'
    assert url in context.testable_urls, f'Unknown URL requested: {url}'
    context.current_url = url
    context.response = context.client.get(url, follow=True)
    context.remaining_urls.discard(url)


@then('the response should return a successful status code')
def assert_successful_status_codes(context):
    response = getattr(context, 'response', None)
    assert response is not None, 'No response recorded for this scenario.'
    assert response.status_code <= SUCCESS_MAX_STATUS, (
        f"{context.current_url} -> {response.status_code}"
    )
