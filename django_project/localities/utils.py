# -*- coding: utf-8 -*-
from django.template import Template, Context


def render_fragment(template, context):
    t = Template(template)
    c = Context(context)
    return t.render(c)
