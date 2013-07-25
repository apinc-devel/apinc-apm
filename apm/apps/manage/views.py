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

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model as Person
from django.utils.translation import ugettext as _

from apm.apps.members.models import Role
from apm.apps.manage.models import Group
from apm.apps.manage.forms import GroupMembershipForm
from apm.decorators import access_required

@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def index(request):

    """manage index"""

    return render(request, 'manage/index.html')


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def members(request):

    """list all APINC members"""
    
    return render(request, 'manage/members.html', { 'members': Person().objects.all() })


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def roles(request):

    """list all APINC roles"""

    messages.add_message(request, messages.INFO, _('Following are listed organization board member roles.'))    
    return render(request, 'manage/roles.html', { 'roles': Role.objects.all() })


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def groups(request):

    """list all apm groups"""

    messages.add_message(request, messages.INFO, _('Following are listed all apinc-apm groups used to manage permissions on apinc-apm application. These groups are handled statically.'))    
    return render(request, 'manage/groups.html', { 'groups': Group.objects.all() })


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def groupmembership_edit(request, user_id=None, gm_id=None):

    """edit apm group membership"""

    gm = None
    form = GroupMembershipForm(member_id=user_id)
    #msg_log = "Payment has been successfully created."
    #title = _('Adding a subscription for')

    person = None
    if user_id:
        person = get_object_or_404(Person(), id=user_id)

    if gm_id:
        gm = get_object_or_404(GroupMembership, id=gm_id)
        form = GroupMembershipForm(instance=gm, member_id=user_id)
        msg_log = "Apm group membership modified."

    if request.method == 'POST':
        if gm_id:
            form = GroupMembershipForm(request.POST, instance=payment,
                    member_id=user_id)
        else:
            form = GroupMembershipForm(request.POST, member_id=user_id)

        if form.is_valid():
            gm = form.save()
            #LogEntry.objects.log_action(
            #    user_id = request.user.id,
            #    content_type_id = ContentType.objects.get_for_model(payment).pk,
            #    object_id = payment.pk, message = msg_log)

            messages.add_message(request, messages.SUCCESS,
                _('Apm group membership has been successfully saved.'))
            return redirect('apm.apps.members.views.details', user_id=gm.member.id)


    return render(request, 'manage/group_membership_edit.html', {
        'form': form, 'person': person,
        'back': request.META.get('HTTP_REFERER','/')})

