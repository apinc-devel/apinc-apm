# -*- coding: utf-8
"""
apinc/association/urls.py
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

urlpatterns = patterns('apinc.association.views',

    # Association

    # pages particulieres au contenu pseudo-statique
    url(r'^$', 'index', name='association'),
    url(r'^status/$', 'status', name='status'),
    url(r'^charter/$', 'charter', name='charter'),

    url(r'^report/upload/$', 'upload_report'),
    url(r'^report/(?P<report_id>\d+)/delete/$', 'delete_report'),
    url(r'^status/pdf/$', 'status_pdf'),
    url(r'^board/$', 'board'),
)
