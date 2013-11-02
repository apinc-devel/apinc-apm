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

from apm.apps.members.models import Person

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def unprivileged_user(username, groups=None):
    from django.conf import settings # ici limiter la visibilité des settings

    p = get_or_none(Person, username=username)

    if not p:
        return True

    if p.is_superuser:
        return False

    user_groups = p.group_set.values_list('name', flat=True)

    if settings.PORTAL_ADMIN in user_groups:
        return False

    if not groups:
        return True

    for group in user_groups:
        if group in groups:
            # Go to the decorated view
            return False

    return True

