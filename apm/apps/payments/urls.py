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

urlpatterns = patterns('apm.apps.payments.views',

    # Contributions

    url(r'^$', 'payments'),
    url(r'^list/(?P<user_id>\d+)/$','user_payments'),
    url(r'^details/(?P<payment_id>\d+)/$','payment_details'),
    url(r'^add/$', 'payment_edit'),
    url(r'^add/user/(?P<user_id>\d+)/$', 'payment_edit'),
    url(r'^edit/(?P<user_id>\d+)/(?P<payment_id>\d+)/$', 'payment_edit'),
    url(r'^delete/(?P<payment_id>\d+)/$', 'payment_delete'),
    url(r'^pay/(?P<contribution_id>\d+)/$', 'pay'),
    url(r'^paypal/create/(?P<contribution_id>\d+)/$', 'paypal_create'),
    url(r'^paypal/execute/(?P<contribution_id>\d+)/(?P<uuid>[0-9a-fA-F]{32})/$', 'paypal_execute'),
    url(r'^paypal/cancel/(?P<uuid>[0-9a-fA-F]{32})/$', 'paypal_cancel'),
    #url(r'^request/$', 'subscription_request'),
)
