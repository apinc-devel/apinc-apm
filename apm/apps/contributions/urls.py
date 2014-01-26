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

from django.conf.urls import *

urlpatterns = patterns('apm.apps.contributions.views',

    # Contributions

    url(r'^list/all/$','contributions', name='all_contributions'),
    #url(r'^pending/list/$','subscriptions', {'to_validate': True},
    #    name='to_validate_subscriptions'),
    url(r'^list/(?P<user_id>\d+)/$','user_contributions'),
    url(r'^add/$', 'contribution_edit'),
    url(r'^add/(?P<user_id>\d+)/$', 'contribution_edit'),
    url(r'^edit/(?P<user_id>\d+)/(?P<contribution_id>\d+)/$', 'contribution_edit'),
    #url(r'^regularize/(?P<user_id>\d+)/$', 'regularize_user'),
    url(r'^validate/(?P<contribution_id>\d+)/$', 'contribution_validate'),
    url(r'^delete/(?P<contribution_id>\d+)/$', 'contribution_delete'),
    url(r'^types/$', 'contribution_types'),
    url(r'^type/add/$', 'contribution_type_edit'),
    url(r'^type/edit/(?P<contribution_type_id>\d+)/$', 'contribution_type_edit'),
    url(r'^type/delete/(?P<contribution_type_id>\d+)/$', 'contribution_type_delete'),
    url(r'^receipt/(?P<user_id>\d+)/(?P<contribution_id>\d+)/$', 'contribution_receipt'),
    url(r'^pay/(?P<user_id>\d+)/$','pay_subscription'),
    #url(r'^request/$', 'subscription_request'),
)
