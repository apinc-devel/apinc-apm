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
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from apinc.members.models import Person, PersonPrivate, Member, Address
from apinc.members.forms import UserForm, PersonForm, PersonPrivateForm, AddressForm
from apinc.decorators import access_required, confirm_required

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

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
def edit(request, user_id=None):
    member = None           
                                
    person = get_object_or_404(Person, pk=user_id)
    personprivate = get_object_or_404(PersonPrivate, person=person)

    if Member.objects.filter(person=person).count() > 0:
        member = get_object_or_404(Member, person=person)
                                     
    return render(request, 'members/edit.html',
        {'person': person, 'member': member, 
         'personprivate': personprivate,
         'is_myself': int(request.user.id) == int(user_id)})

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
def user_edit(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid(): 
            form.save()
            request.user.message_set.create(message=
                _('User modifications have been successfully saved.'))
        
        return HttpResponseRedirect(reverse(edit, args=[user_id]))
    
    return render(request, 'members/edit_form.html',
        {'form': form, 'action_title': _("Modification of user profile for"),
         'person': user.person, 'back': request.META.get('HTTP_REFERER', '/')})

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
def person_edit(request, user_id=None):
    person = get_object_or_404(Person, pk=user_id)
    form = PersonForm(instance=person)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid(): 
            form.save()
            request.user.message_set.create(message=
                _('Person modifications have been successfully saved.'))
        
        return HttpResponseRedirect(reverse(edit, args=[user_id]))
    
    return render(request, 'members/edit_form.html',
        {'form': form, 'action_title': _("Modification of personal profile for"),
         'person': person, 'back': request.META.get('HTTP_REFERER', '/')})

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
def personprivate_edit(request, user_id=None):
    personprivate = PersonPrivate.objects.get(person=user_id)
    form = PersonPrivateForm(instance=personprivate)

    if request.method == 'POST':
        form = PersonPrivateForm(request.POST, instance=personprivate)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message=
                _('PersonPrivate modification have been successfully saved.'))

        return HttpResponseRedirect(reverse(edit, args=[user_id]))

    return render(request, 'members/edit_form.html',
            {'form': form,
             'action_title': _('Modification of personal private profile for'),
             'person': personprivate.person,
             'back': request.META.get('HTTP_REFERER', '/')})

def member_edit(request, user_id=None):
    return #FIXME

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
def address_edit(request, user_id=None, address_id=None):
    person = get_object_or_404(Person, user=user_id)
    address = None
    title = _('Creation of an address for')
    form = AddressForm()

    if address_id:
        address = get_object_or_404(Address, pk=address_id)
        form = AddressForm(instance=address)

        title = _('Modification of an address for')
                                 
    if request.method == 'POST': 
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            adr = form.save(commit=False)
            adr.person = person 
            adr.save()          
                                
            request.user.message_set.create(message= 
                _('Address modification have been successfully saved.'))

            return HttpResponseRedirect(reverse(edit, args=[user_id]))

    return render(
        request, 'members/edit_form.html',
        {'form': form, 'action_title': title, 'person': person,
         'back': request.META.get('HTTP_REFERER', '/')})

@access_required(groups=['apinc-secretariat', 'apinc-bureau'], allow_myself=True)
@confirm_required(lambda user_id=None, address_id=None :
    str(get_object_or_404(Address, pk=address_id)), 'members/base_members.html', 
    _('Do you really want to delete this address'))
def address_delete(request, user_id=None, address_id=None):
    """Address delete"""

    address = get_object_or_404(Address, pk=address_id)
    address.delete()

    request.user.message_set.create(message=
        _('The address has been successfully deleted.'))
    return HttpResponseRedirect(reverse(edit, kwargs={'user_id': user_id}))
