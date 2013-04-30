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

from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from apm.apps.groups.models import Group
from apm.decorators import access_required

@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def index(request):
    groups = Group.objects.all()
    return render(request, 'groups/index.html', {'groups': groups})
