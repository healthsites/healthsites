#!/usr/bin/env python
# coding=utf-8
"""
django_app.manage
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
