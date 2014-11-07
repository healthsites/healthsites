# -*- coding: utf-8 -*-
from django.template import Template, Context


def render_fragment(template, context):
    t = Template(template)
    c = Context(context)
    return t.render(c)


def detect_data_changes(original_data, changed_data):
    """
    Compare original data and changed data dictionaries, return a list of keys
    that do not exists in the original data and those with values that differ
    in changed data
    """
    return dict(
        set(changed_data.items()).difference(set(original_data.items()))
    ).keys()


def ramify_data(initial_data, candidate_keys):
    """
    Iterate over initial_data dictionary and ramify into distinct dictionaries
    based on candidate_keys
    """
    loc_data = {}
    values_data = {}
    for key, val in initial_data.iteritems():
        if key in candidate_keys:
            loc_data.update({key: val})
        else:
            values_data.update({key: val})

    return (loc_data, values_data)
