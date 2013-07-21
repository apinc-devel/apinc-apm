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

from django.conf.urls.defaults import *

urlpatterns = patterns('apm.apps.payments.views',

    # Contributions

    url(r'^$', 'payments'),
    url(r'^list/(?P<user_id>\d+)/$','user_payments'),
    url(r'^add/$', 'payment_edit'),
    url(r'^add/(?P<user_id>\d+)/$', 'payment_edit'),
    url(r'^edit/(?P<user_id>\d+)/(?P<payment_id>\d+)/$', 'payment_edit'),
    url(r'^delete/(?P<payment_id>\d+)/$', 'payment_delete'),
    url(r'^distribute/(?P<payment_id>\d+)/$', 'payment_distribute'),
    #url(r'^request/$', 'subscription_request'),
)
