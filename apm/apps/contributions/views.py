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

import time
from cStringIO import StringIO
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.contributions.models import Contribution, ContributionType
from apm.apps.contributions.forms import ContributionForm, ContributionTypeForm
from apm.decorators import access_required, confirm_required
from apm.utils import unprivileged_user


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
@confirm_required(lambda contribution_type_id=None :
    str(get_object_or_404(ContributionType, pk=contribution_type_id)),
    'manage/base_manage.html',
    _('Do you really want to delete this contribution type'))
def contribution_type_delete(request, contribution_type_id=None):

    """delete a contribution type"""

    contribution_type = get_object_or_404(ContributionType, pk=contribution_type_id)
    contribution_type.delete()
    messages.add_message(request, messages.SUCCESS, _('Contribution type successfully deleted'))

    return redirect(contribution_types)


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
    title = _('Adding a contribution')

    person = None
    if user_id:
        person = get_object_or_404(Person, id=user_id)
        if not person.get_first_subscription_date():
            messages.add_message(request, messages.INFO, _('Person is not elligible for membership.' + \
                                                           ' You may check if person owns an APINC VHFFS project.'))

            return HttpResponseRedirect(reverse('apm.apps.members.views.details', kwargs={'user_id':user_id}))
        
    if contribution_id:
        contribution = get_object_or_404(Contribution, id=contribution_id)
        if unprivileged_user(request.user.username) and contribution.validated:
            return render(request, 'auth/permission_denied.html', {})

        form = ContributionForm(instance=contribution,
                     person_id=contribution.person.id)
        title = _('Contribution editor')
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

                if not contribution.subscription_start_date:
                    messages.add_message(request, messages.WARNING,
                        _('No project found for member %s' % contribution.person))
                    page_dict.update({'form': form})
                    return render(request, 'contributions/contribution_edit.html', page_dict)

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


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'],
        allow_myself=True)
def contribution_receipt(request, user_id=None, contribution_id=None):

    """generate pdf receipt for a validated contribution"""

    from django.conf import settings # import here to limit settings visibility

    person = get_object_or_404(Person, id=user_id)
    contribution = get_object_or_404(Contribution, pk=contribution_id)
    if not contribution.validated:
        messages.add_message(request, messages.ERROR, _('Contribution is not yet validated.'))
        return redirect(request.POST.get('next', '/'))

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="apinc-receipt.pdf"'

    receipt_buffer = StringIO()

    doc = SimpleDocTemplate(receipt_buffer,pagesize=A4,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    apinc_receipt=[]
    logo = settings.STATIC_ROOT + "images/entete_recu.png"
     
    full_name = "%s %s" % (person.last_name, person.first_name)
    address_parts = ["c/o FFCU", "173 rue de Charenton", "75012, PARIS"]
     
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles["Justify"].leading = 30
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    # logo header
    im = Image(logo)
    apinc_receipt.append(im)

    apinc_receipt.append(Spacer(1, 48))

    # title 
    ptext = '<font size=18>Attestation de reçu de %s</font>'.decode('utf-8', 'ignore') % contribution.type.label.lower()
    apinc_receipt.append(Paragraph(ptext, styles["Center"]))

    apinc_receipt.append(Spacer(1, 48))

    # body 
    apinc_receipt.append(Spacer(1, 12))
    ptext = '<font size=12>Je soussigné FIXME FIXME, trésorier de l\'APINC, certifie que %(lastname)s %(firstname)s a versé la somme de %(amount)s euros en date du %(date)s en règlement d\'une %(contribution_type)s.</font>'.decode('utf-8', 'ignore') % ({'lastname': person.last_name, 'firstname': person.first_name, 'amount': contribution.dues_amount, 'date': contribution.payments.all()[0].date.strftime('%Y-%m-%d'), 'contribution_type': contribution.type.label.lower()})
    apinc_receipt.append(Paragraph(ptext, styles["Justify"]))

    apinc_receipt.append(Spacer(1, 100))

    # date
    ptext = '<font size=12>Fait à Paris, le %s.</font>' % datetime.datetime.now().strftime('%Y-%m-%d')
    apinc_receipt.append(Paragraph(ptext, styles["Normal"]))

    apinc_receipt.append(Spacer(1, 12))
     
    # Create return address
    #ptext = '<font size=12>%s</font>' % full_name
    #apinc_receipt.append(Paragraph(ptext, styles["Normal"]))       
    #for part in address_parts:
    #    ptext = '<font size=12>%s</font>' % part.strip()
    #    apinc_receipt.append(Paragraph(ptext, styles["Normal"]))   
     
     
    # Create footer 
    apinc_receipt.append(Spacer(1, 200))
    ptext = '<font size=10><b>APINC - Association Pour l\'Internet Non Commercial</b><br/>' + \
            'Association loi de 1901.<br/>' + \
            'Numero SIREN : 448 004 556 Numero CNIL : 783317<br/>' + \
            'Siege social : APINC c/o FFCU<br/>' + \
            '173 rue de Charenton, 72012 PARIS<br/>' + \
            'http://www.apinc.org</font>'
    apinc_receipt.append(Paragraph(ptext, styles["Normal"]))
    doc.build(apinc_receipt)    

    response.write(receipt_buffer.getvalue())
    receipt_buffer.close()

    return response

#@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
#def regularize_user(request, user_id=None):
#
#    """regularize user subscriptions"""
#
#    person = get_object_or_404(Person, id=user_id)
#    #member = get_object_or_404(Member, person=person)
#
#    if person.is_subscriber():
#        messages.add_message(request, messages.INFO, _('No need to regularize, member has a valid subscription.'))
#        return redirect(user_subscriptions, user_id=user_id)
#    if person.pending_subscriptions():
#        messages.add_message(request, messages.INFO, _('No need to regularize, member has a pending subscription.'))
#        return redirect(user_subscriptions, user_id=user_id)
#
#    last_subscription_end_date = person.last_subscription_end_date()
#    if not last_subscription_end_date:
#        last_subscription_end_date = datetime.date.today()
#
#    subscription = Subscription()
#    subscription.dues_amount = 0
#    subscription.payment = None
#    subscription.tender_type = Subscription.OTHER
#    subscription.start_date = datetime.date(
#        datetime.date.today().year,
#        last_subscription_end_date.month,
#        last_subscription_end_date.day)
#    subscription.end_date = datetime.date(
#        datetime.date.today().year + 1,
#        last_subscription_end_date.month,
#        last_subscription_end_date.day)
#    subscription.date = datetime.datetime.now()
#    subscription.validated = True
#    subscription.member = person
#    subscription.save()
#
#    messages.add_message(request, messages.SUCCESS, _('The member subscription has been successfully regularized.'))
#
#    return redirect(user_subscriptions, user_id=user_id)
#
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
