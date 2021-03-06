# -*- coding: utf-8 -*-
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

from django.conf.urls import *

urlpatterns = patterns('apm.apps.manage.views',

    # Manage

    url(r'^$','index'),
    url(r'^members/$','members'),
    url(r'^roles/$','roles'),
    url(r'^groups/$','groups'),
    url(r'^groupmembership/delete/(?P<gm_id>\d+)/$','groupmembership_delete'),
    url(r'^groupmembership/add/(?P<user_id>\d+)/$','groupmembership_edit'),
    url(r'^groupmembership/edit/(?P<user_id>\d+)/(?P<gm_id>\d+)/$','groupmembership_edit'),
)
