# -*- coding: utf-8
"""
apinc/news/urls.py
"""
#
#   Copyright © 2011 APINC Devel Team
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
#

from django.conf.urls.defaults import *
from apinc.news.models import News

urlpatterns = patterns('apinc.news.views',

    # News

    url(r'^$','index'),
    url(r'^add/$', 'edit'),
    url(r'^drafts/$', 'drafts'),
    url(r'^details/(?P<news_slug>[\w\-]+)/$', 'details'),
    url(r'^edit/(?P<news_slug>[\w\-]+)/$', 'edit'),
    url(r'^delete/(?P<news_slug>[\w\-]+)/$', 'delete'),
    url(r'^(?P<year>\d{4})/$', 'published', name='news_year_archives'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'published',
        name='news_month_archives'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        'published', name='news_day_archives'),
)
