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

import datetime
from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.contributions.models import Contribution, ContributionType
from apm.apps.contributions.forms import ContributionForm, ContributionTypeForm
from apm.decorators import access_required, confirm_required


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def contribution_types(request):

    """Types of contributions"""

    return render(request, 'contributions/contribution_types.html',
        {'type_list': ContributionType.objects.all()})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def contribution_type_edit(request, contribution_type_id=None):

    """add/edit contribution type"""

    contribution_type = None
    form = ContributionTypeForm()
    msg_log = "Contribution type created."

    if contribution_type_id:
        contribution_type = get_object_or_404(ContributionType, id=contribution_type_id)
        form = ContributionTypeForm(instance=contribution_type)
        msg_log = "Contribution type modified."

    if request.method == 'POST':
        if contribution_type_id:
            form = ContributionTypeForm(request.POST, instance=contribution_type)
        else:
            form = ContributionTypeForm(request.POST)

        if form.is_valid():
            contribution_type = form.save()
            #LogEntry.objects.log_action(
            #    user_id = request.user.id,
            #    content_type_id = ContentType.objects.get_for_model(contribution_type).pk,
            #    object_id = contribution_type.pk, message = msg_log)
 
            messages.add_message(request, messages.SUCCESS,
                _('Contribution type has been successfully saved.'))
            return redirect(contribution_types)

    return render(request, 'contributions/contribution_type_edit.html', {
        'form': form, 'contribution_type': contribution_type,
        'back': request.META.get('HTTP_REFERER','/')})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def contributions(request, to_validate=False):

    """list contributions"""

    nb_results_by_page = 50
    contributions_list = Contribution.objects.all()
    
    if to_validate:
        contributions_list = contributions_list.filter(validated=False)

    paginator = Paginator(contributions_list, nb_results_by_page)

    page = request.GET.get('page', 1)
    try:
        contributions_list = paginator.page(page).object_list
    except InvalidPage:
        raise Http404

    return render(request, 'contributions/contributions.html',
        {'contributions_list': contributions_list,
         'to_validate': to_validate,
         'paginator': paginator, 'is_paginated': paginator.num_pages > 1,
         'has_next': paginator.page(page).has_next(),
         'has_previous': paginator.page(page).has_previous(),
         'current_page': page, 'pages': paginator.num_pages,
         'next_page': page + 1, 'previous_page': page - 1,
         'first_result': (page-1) * nb_results_by_page +1,
         'last_result': min((page) * nb_results_by_page, paginator.count),
         'hits': paginator.count})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'],
        allow_myself=True)
def contribution_edit(request, user_id=None, contribution_id=None):

    """add/edit user contribution (subscription, donation,...)"""

    contribution = None
    today = datetime.date.today()
    form = ContributionForm(person_id=user_id)
    msg_log = "Contribution has been successfully created."
    title = _('Adding a subscription for')

    person = None
    if user_id:
        person = get_object_or_404(Person, id=user_id)

    if contribution_id:
        contribution = get_object_or_404(Contribution, id=contribution_id)
        if contribution.validated == True:
            return render(request, 'auth/permission_denied.html', {})

        form = ContributionForm(instance=contribution,
                     person_id=contribution.person.id)
        title = _('Editing a subscription for')
        msg_log = "Contribution has been successfully modified."

    page_dict = {'action_title': title, 'person': person,
        'types': ContributionType.objects.active(),
        'back': request.META.get('HTTP_REFERER', '/')}

#    if request.method == 'GET':
#        if Contribution.objects.filter(person=person).exclude(
#            start_date__gt=today).exclude(end_date__lt=today):
            #messages.add_message(request, messages.INFO, _('You already have an active subscription.'))

    if request.method == 'POST':
        if contribution_id:
            form = ContributionForm(request.POST, request.FILES,
                     instance=contribution, person_id=contribution.person.id)
        else:
            form = ContributionForm(request.POST, request.FILES)

        if form.is_valid():
            contribution = form.save(commit=False)
            if contribution.type.extends_duration:
                contribution.subscription_start_date = contribution.person\
                                            .get_next_subscription_start_date()
                contribution.subscription_end_date = contribution\
                    .subscription_start_date + relativedelta(
                     months=contribution.type.extends_duration, days=-1)
            contribution.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _(msg_log))

            # TODO payment
            
            # TODO send email to user
            
            # TODO si payment par card (tender_type) vérifier avec l'api de la banque ?

            return redirect(user_contributions, user_id=contribution.person.id)
            
    page_dict.update({'form': form})
    return render(request, 'contributions/contribution_edit.html', page_dict)


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
@confirm_required(lambda contribution_id=None :
    str(get_object_or_404(Contribution, pk=contribution_id)),
    'manage/base_manage.html',
    _('Do you really want to validate this contribution'))
def contribution_validate(request, contribution_id=None):

    """validate a contribution"""

    contribution = get_object_or_404(Contribution, pk=contribution_id)
    contribution.validated = True
    contribution.save()
    messages.add_message(request, messages.SUCCESS, _('Contribution successfully validated.'))
    return redirect(request.POST.get('next', '/'))


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
@confirm_required(lambda contribution_id=None :
    str(get_object_or_404(Contribution, pk=contribution_id)),
    'manage/base_manage.html',
    _('Do you really want to delete this contribution'))
def contribution_delete(request, contribution_id=None):

    """delete a contribution"""

    contribution = get_object_or_404(Contribution, pk=contribution_id)
    contribution.delete()
    messages.add_message(request, messages.SUCCESS, _('Contribution successfully deleted.'))
    return redirect(request.POST.get('next', '/'))

@access_required(groups=['apinc-secretariat', 'apinc-tresorier'],
        allow_myself=True)
def user_contributions(request, user_id=None):

    """show user contributions"""

    person = get_object_or_404(Person, id=user_id)

    contributions_list = Contribution.objects.filter(person=person)

    return render(request, 'contributions/user_contributions.html',
        {'person': person,
        'contributions_list': contributions_list})
        #'is_subscriber': person.is_subscriber()})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def regularize_user(request, user_id=None):

    """regularize user subscriptions"""

    person = get_object_or_404(Person, id=user_id)
    #member = get_object_or_404(Member, person=person)

    if person.is_subscriber():
        messages.add_message(request, messages.INFO, _('No need to regularize, member has a valid subscription.'))
        return redirect(user_subscriptions, user_id=user_id)
    if person.pending_subscriptions():
        messages.add_message(request, messages.INFO, _('No need to regularize, member has a pending subscription.'))
        return redirect(user_subscriptions, user_id=user_id)

    last_subscription_end_date = person.last_subscription_end_date()
    if not last_subscription_end_date:
        last_subscription_end_date = datetime.date.today()

    subscription = Subscription()
    subscription.dues_amount = 0
    subscription.payment = None
    subscription.tender_type = Subscription.OTHER
    subscription.start_date = datetime.date(
        datetime.date.today().year,
        last_subscription_end_date.month,
        last_subscription_end_date.day)
    subscription.end_date = datetime.date(
        datetime.date.today().year + 1,
        last_subscription_end_date.month,
        last_subscription_end_date.day)
    subscription.date = datetime.datetime.now()
    subscription.validated = True
    subscription.member = person
    subscription.save()

    messages.add_message(request, messages.SUCCESS, _('The member subscription has been successfully regularized.'))

    return redirect(user_subscriptions, user_id=user_id)

#@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
#def subscription_type_edit(request, type_id=None):
#    
#    """edit subscription type"""
#
#    form = ContributionTypeForm()
#
#    if type_id:
#        subscription_type = get_object_or_404(SubscriptionType, pk=type_id)
#        form = SubscriptionTypeForm(instance=subscription_type)
#
#    if request.method == 'POST':
#        if type_id:
#            form = SubscriptionTypeForm(request.POST,
#                instance=subscription_type)
#        else:
#            form = SubscriptionTypeForm(request.POST)
#        if form.is_valid():
#            form.save()
#            messages.add_message(request, messages.SUCCESS, _("Modifications on subscription type have been \
#successfully saved."))
#            return redirect(subscription_types)
#            
#    return render(request, 'contributions/subscription_type_edit.html',
#            {'form': form, 
#             'back': request.META.get('HTTP_REFERER', '/')})

@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
@confirm_required(lambda type_id=None :
    str(get_object_or_404(ContributionType, pk=type_id)),
    'manage/base_manage.html',
    _('Do you really want to delete this contribution type'))
def contribution_type_delete(request, type_id=None):

    """delete a contribution type"""

    contribution_type = get_object_or_404(ContributionType, pk=type_id)
    contribution_type.delete()
    messages.add_message(request, messages.SUCCESS, _('Contribution type successfully deleted'))

    return redirect(contribution_types)


def subscription_request(request):
    # TODO
    return render(request, 'contributions/request.html')

