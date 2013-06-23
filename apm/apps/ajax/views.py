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

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder

from apm.apps.contributions.models import ContributionType

@login_required
def ajax_contribution_type(request, contribution_type_id):
    if not request.is_ajax():
        raise Http404

    contribution_type = get_object_or_404(ContributionType, id=contribution_type_id)

    if not contribution_type.active:
        raise Http404
        
    response = []
    if request.method == 'POST':
        response.append( {'dues_amount': contribution_type.dues_amount,
            'extends_duration': contribution_type.extends_duration } )

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
            content_type="application/json")
