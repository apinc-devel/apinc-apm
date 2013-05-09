# -*- coding: utf-8 -*-
#
#   Copyright © 2011-2013 APINC Devel Team
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from django.db import models
from django.contrib.sitemaps import Sitemap
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic

from apm.apps.news.utils import get_available_slug
from apm.manage.models import LogEntry

DRAFT = 0
PUBLISHED = 1

class NewsManager(models.Manager):
    def published(self, period=None):
        if period:
            return self.filter(**period).filter(status__exact=PUBLISHED)
        else :
            return self.filter(status__exact=PUBLISHED)

    def drafted(self):
        return self.filter(status__exact=DRAFT)

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='Automatically built from the title.'
    )
    body_html = models.TextField(blank=True)
    pub_date = models.DateTimeField('Date published')
    PUB_STATUS = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )
    status = models.IntegerField(choices=PUB_STATUS, default=0)
    logs = generic.GenericRelation(LogEntry)

    objects = NewsManager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        if self.status == PUBLISHED:
            return ('apm.apps.news.views.published_details', [str(self.slug)])
        else:
            return ('apm.apps.news.views.draft_details', [str(self.slug)])

    def get_previous_published(self):
        return self.get_previous_by_pub_date(status__exact=PUBLISHED)

    def get_next_published(self):
        return self.get_next_by_pub_date(status__exact=PUBLISHED)

    def get_previous_drafted(self):
        return self.get_previous_by_pub_date(status__exact=DRAFT)

    def get_next_drafted(self):
        return self.get_next_by_pub_date(status__exact=DRAFT)

    def is_published(self):
        return self.status == PUBLISHED

    def save(self, *args, **kwargs):
        """News save method"""
        if not self.id:
            # Newly created object, so set slug
            self.slug = get_available_slug(self.title)

        super(News, self).save(*args, **kwargs)
