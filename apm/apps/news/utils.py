# -*- coding: utf-8 -*-

# Inspired from https://github.com/divio/django-cms/blob/develop/cms/utils/page.py

import re

from django.template.defaultfilters import slugify

APPEND_TO_SLUG = "-copy"
COPY_SLUG_REGEX = re.compile(r'^.*-copy(?:-(\d)*)?$')
iOPY_SLUG_REGEX = re.compile(r'^.*-copy(?:-(\d)*)?$')

def is_valid_news_slug(slug):
    """Validates given slug depending on existing news.
    """
    try:
        from apm.apps.news.models import News
        News.objects.get(slug=slug)
        return False
    except News.DoesNotExist as e:
        return True

def get_available_slug(title, new_slug=None):
    """Smart function generates slug for title if current title slug cannot be
    used. Appends APPEND_TO_SLUG to slug and checks it again.

    Returns: slug
    """
    rewrite_slug = False
    slug = new_slug or slugify(title)
    # This checks for conflicting slugs
    if not is_valid_news_slug(slug):
        # add nice copy attribute, first is -copy, then -copy-2, -copy-3, ....
        match = COPY_SLUG_REGEX.match(slug)
        if match:
            try:
                next = int(match.groups()[0]) + 1
                slug = "-".join(slug.split('-')[:-1]) + "-%d" % next
            except TypeError:
                slug += "-2"

        else:
            slug += APPEND_TO_SLUG
        return get_available_slug(title, slug)
    else:
        return slug
