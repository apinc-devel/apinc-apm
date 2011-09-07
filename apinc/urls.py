# -*- coding: utf-8
"""
apinc/urls.py
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

from django.conf import settings
from django.conf.urls.defaults import *

# Décommenter les deux lignes ci-dessous pour servir l'admin (django)
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Décommenter la ligne ci-dessous pour servir l'admin (django)
    #(r'^admin/', include(admin.site.urls)),

    # servir le contenu statique pendant le dev
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    # Pages particulieres au contenu pseudo statique
    (r'^$', 'pages.views.homepage', {}, 'homepage'),
    (r'^about/$', 'apinc.pages.views.page', { 'page': "about" }, 'about'),
    (r'^charte/$', 'apinc.pages.views.page', { 'page': "charte" }, 'charte'),
    (r'^contact/$', 'apinc.pages.views.page', { 'page': "contact" },
        'contact'),
    (r'^legal-notice/$', 'apinc.pages.views.page', { 'page': "legal-notice" },
        'legal-notice'),
    (r'^edit/(?P<page>[\w\-]+)/$', 'apinc.pages.views.edit'),

    # Account authentication section
    (r'^accounts/login/$', 'apinc.pages.views.login'),
    (r'^accounts/logout/$', 'apinc.pages.views.logout'),

    (r'^members/', include('apinc.members.urls')),

    (r'^groups/', include('apinc.groups.urls')),

    (r'^news/', include('apinc.news.urls')),

    (r'^association/', include('apinc.association.urls')),
)
