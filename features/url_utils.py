"""Helpers for collecting project-owned Django URL patterns."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Union

from django.urls import URLPattern, URLResolver, get_resolver
from django.urls.resolvers import RegexPattern, RoutePattern

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DJANGO_PROJECT_ROOT = PROJECT_ROOT / 'django_project'


def _is_parameterized(pattern: URLPattern) -> bool:
    fragment = pattern.pattern
    if isinstance(fragment, RoutePattern):
        return bool(fragment.converters)
    return fragment.regex.groups > 0


def _pattern_to_text(
    pattern_fragment: Union[RoutePattern, RegexPattern]
) -> str:
    if isinstance(pattern_fragment, RoutePattern):
        return pattern_fragment.pattern
    text = pattern_fragment.regex.pattern
    return text.lstrip('^').rstrip('$')


def _normalise(path: str) -> str:
    if not path:
        return '/'
    return '/' + path.lstrip('/')


def _resolver_is_project_owned(resolver: URLResolver) -> bool:
    module = resolver.urlconf_module
    modules = module if isinstance(module, (list, tuple)) else [module]
    for candidate in modules:
        module_file = getattr(candidate, '__file__', None)
        if module_file is None:
            return True
        try:
            Path(module_file).resolve().relative_to(DJANGO_PROJECT_ROOT)
            return True
        except ValueError:
            continue
    return False


def _collect_urls(patterns: Iterable, prefix: str = '') -> List[str]:
    """Recursively collect URL patterns that do not require parameters."""
    collected: List[str] = []
    for entry in patterns:
        if isinstance(entry, URLPattern):
            if _is_parameterized(entry):
                continue
            fragment = _pattern_to_text(entry.pattern)
            collected.append(_normalise(prefix + fragment))
        elif isinstance(entry, URLResolver):
            if not _resolver_is_project_owned(entry):
                continue
            fragment = _pattern_to_text(entry.pattern)
            collected.extend(_collect_urls(entry.url_patterns, prefix + fragment))
    return collected


def collect_testable_urls() -> List[str]:
    resolver = get_resolver()
    return sorted(set(_collect_urls(resolver.url_patterns)))
