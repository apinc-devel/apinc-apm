#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # inspired from http://lincolnloop.com/django-best-practices/projects.html#settings
    # see also https://code.djangoproject.com/wiki/SplitSettings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apm.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
