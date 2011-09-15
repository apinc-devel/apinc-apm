# -*- coding: utf-8
"""
 apinc/members/views.py
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

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from apinc.members.models import Person, PersonPrivate

@login_required
def details(request, user_id):

    is_myself = int(request.user.id) == int(user_id)

    person = get_object_or_404(Person, pk=user_id)
    personprivate = get_object_or_404(PersonPrivate, person=person)

#FIXME
#    if UserActivity.objects.filter(person=person):
#        last_activity = UserActivity.objects.filter(person=person).latest('id')

    return render(request, 'members/details.html',
        {'person': person, 'personprivate': personprivate, 
         'is_myself': is_myself}) #, 'last_activity': last_activity})

