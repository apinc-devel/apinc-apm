# -*- coding: utf-8
"""
apinc/context_processors.py
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

import datetime

from django.conf import settings

from apinc.members.models import Person

def base(request):
    """ Returns the current year """
    return {
        'current_year'       : datetime.date.today().year,
        'apinc_siren'        : settings.APINC_SIREN,
        'apinc_cnil'         : settings.APINC_CNIL,
    }

def versions(request):
    return {
        'portal_version'     : settings.VERSION,
        'jquery_version'     : settings.JQUERY_VERSION,
    }

def user_groups(request):

    user_groups = []

    if (request.user.is_authenticated() and
        Person.objects.filter(user=request.user)):
            user_groups = request.user.person.groups.values_list('group__name', flat=True)

    return {
        'superadmin'         : settings.APINC_PORTAL_ADMIN in user_groups,
        'secretariat_member' : 'apinc-secretariat' in user_groups,
        'bureau_member'      : 'apinc-bureau' in user_groups,
        'secretariat_member' : 'apinc-secretariat' in user_groups,
        'contributeur'       : 'apinc-contributeur' in user_groups,
    }
