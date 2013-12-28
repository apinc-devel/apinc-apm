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

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import get_user_model as Person

from apm.apps.members.models import PersonPrivate, MemberRole, Project
from apm.apps.members.forms import PersonForm, PersonPrivateForm, MemberRoleForm
from apm.decorators import access_required, confirm_required

@login_required(login_url=reverse_lazy('apm.apps.pages.views.login'))
def details(request, user_id):

    person = get_object_or_404(Person(), pk=user_id)
    personprivate = get_object_or_404(PersonPrivate, person=person)

#FIXME
#    if UserActivity.objects.filter(person=person):
#        last_activity = UserActivity.objects.filter(person=person).latest('id')

    return render(request, 'members/details.html',
        {'person': person,
         'personprivate': personprivate, 
         'is_myself': int(request.user.id) == int(user_id),
         'projects': Project.objects.get_active_for(person)}) #, 'last_activity': last_activity})

#@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
#def edit(request, user_id=None):
#                                
#    person = get_object_or_404(Person, pk=user_id)
#    personprivate = get_object_or_404(PersonPrivate, person=person)
#
#    return render(request, 'members/edit.html',
#        {'person': person, 
#         'personprivate': personprivate,
#         'is_myself': int(request.user.id) == int(user_id)})

#@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
#def person_edit(request, user_id=None):
#    person = get_object_or_404(Person, pk=user_id)
#    form = PersonForm(instance=person)
#
#    if request.method == 'POST':
#        form = PersonForm(request.POST, instance=person)
#        if form.is_valid(): 
#            form.save()
#            messages.add_message(request, messages.INFO, _('Person modifications have been successfully saved.'))
#            return HttpResponseRedirect(reverse(edit, args=[user_id]))
#
#    return render(request, 'members/edit_form.html',
#        {'form': form, 'action_title': _("Modification of personal profile for"),
#         'person': person, 'back': request.META.get('HTTP_REFERER', '/')})

@access_required(groups=['apinc-secretariat', 'apinc-bureau'])
def personprivate_edit(request, user_id=None):
    personprivate = PersonPrivate.objects.get(person=user_id)
    form = PersonPrivateForm(instance=personprivate)

    if request.method == 'POST':
        form = PersonPrivateForm(request.POST, instance=personprivate)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('PersonPrivate modification have been successfully saved.'))

        return HttpResponseRedirect(reverse(details, args=[user_id]))

    return render(request, 'members/edit_form.html',
            {'form': form,
             'action_title': _('Modification of personal private profile for'),
             'person': personprivate.person,
             'back': request.META.get('HTTP_REFERER', '/')})


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
def member_role_edit(request, user_id=None, mr_id=None):

    """edit member role"""

    mr = None
    form = MemberRoleForm(member_id=user_id)
    person = None
    if user_id:
        person = get_object_or_404(Person(), id=user_id)

    if mr_id:
        mr = get_object_or_404(MemberRole, id=mr_id)
        form = MemberRoleForm(instance=mr, member_id=user_id)
        msg_log = "Member role modified."

    if request.method == 'POST':
        if mr_id:
            form = MemberRoleForm(request.POST, instance=mr,
                    member_id=user_id)
        else:
            form = MemberRoleForm(request.POST, member_id=user_id)

        if form.is_valid():
            mr = form.save()
            #LogEntry.objects.log_action(
            #    user_id = request.user.id,
            #    content_type_id = ContentType.objects.get_for_model(payment).pk,
            #    object_id = payment.pk, message = msg_log)

            messages.add_message(request, messages.SUCCESS,
                _('Member role has been successfully saved.'))
            return redirect('apm.apps.members.views.details', user_id=mr.member.id)


    return render(request, 'members/member_role_edit.html', {
        'form': form, 'person': person,
        'back': request.META.get('HTTP_REFERER','/')})


@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
@confirm_required(lambda mr_id: str(get_object_or_404(MemberRole, id=mr_id)),
        section='members/base_members.html',
        message=_('Do you really want to delete this member role'))
def member_role_delete(request, mr_id):
    """Member role delete"""

    mr = get_object_or_404(MemberRole, id=mr_id)
    mr.delete()

    messages.add_message(request, messages.SUCCESS, _('The member role has been successfully deleted.'))
    return redirect('apm.apps.members.views.details', user_id=mr.member.id)
