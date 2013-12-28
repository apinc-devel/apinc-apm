# -*- coding: utf-8 -*-
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

from django.conf.urls import *

urlpatterns = patterns('apm.apps.members.views',

    # Members

    url(r'^details/(?P<user_id>\d+)/$', 'details'),
    # changecredentials
    # sendcredentials
#    url(r'^edit/(?P<user_id>\d+)/$', 'edit'),
#    url(r'^person/edit/(?P<user_id>\d+)/$', 'person_edit'),
    url(r'^personprivate/edit/(?P<user_id>\d+)/$', 'personprivate_edit'),
    url(r'^member_role/delete/(?P<mr_id>\d+)/$','member_role_delete'),
    url(r'^member_role/add/(?P<user_id>\d+)/$','member_role_edit'),
    url(r'^member_role/edit/(?P<user_id>\d+)/(?P<mr_id>\d+)/$','member_role_edit'),
)
