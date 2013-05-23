# -*- coding:utf-8 -*-
#
#   Copyright © 2013 APINC Devel Team
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

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings

from apm.apps.news.feeds import RssNewsFeed, AtomNewsFeed

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apm.apps.views.home', name='home'),
    # url(r'^apm/', include('apm.apps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

    # Pages particulieres au contenu pseudo statique
    url(r'^$', 'apm.apps.pages.views.homepage', name='homepage'),
    url(r'^about/$', 'apm.apps.pages.views.page', { 'page': "about" },
        name='about'),
    url(r'^contact/$', 'apm.apps.pages.views.page', { 'page': "contact" },
        name='contact'),
    url(r'^legal-notice/$', 'apm.apps.pages.views.page',
        { 'page': "legal-notice" }, name='legal-notice'),

    (r'^edit/(?P<page>[\w\-]+)/$', 'apm.apps.pages.views.edit'),

    # Page particulière client irc
    url(r'^irc/$', 'apm.apps.pages.views.irc', name='irc'),

    # Feeds 
    url(r'^rss/$', RssNewsFeed(), name='news_rss_feed'),
    url(r'^atom/$', AtomNewsFeed(), name='news_atom_feed'),

    # Account authentication section
    (r'^account/login/$', 'apm.apps.pages.views.login'),
    (r'^account/logout/$', 'apm.apps.pages.views.logout'),

    # Apps urls
    (r'^members/', include('apm.apps.members.urls')),
    (r'^news/', include('apm.apps.news.urls')),
    (r'^association/', include('apm.apps.association.urls')),
    (r'^manage/', include('apm.apps.manage.urls')),
)

# servir le contenu statique pendant le dev

# static
# This helper function will only work if DEBUG is True and your STATIC_URL
# setting is neither empty nor a full URL such as http://static.apinc.org/.
urlpatterns += staticfiles_urlpatterns()

# media
if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
