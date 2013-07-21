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

import datetime
from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.payments.models import Payment
from apm.apps.payments.forms import PaymentForm
from apm.decorators import access_required, confirm_required



@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def payments(request):

    """Payments"""

    return render(request, 'payments/payments.html',
        {'payment_list': Payment.objects.all()})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'],
        allow_myself=True)
def user_payments(request, user_id=None):

    """show user payments"""

    person = get_object_or_404(Person, id=user_id)

    payments_list = Payment.objects.filter(emitter=person)

    return render(request, 'payments/user_payments.html',
        {'person': person,
        'payments_list': payments_list})
        #'is_subscriber': person.is_subscriber()})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
def payment_edit(request, user_id=None, payment_id=None):

    """add/edit payment"""

    payment = None
    form = PaymentForm(emitter_id=user_id)
    msg_log = "Payment has been successfully created."
    #title = _('Adding a subscription for')

    person = None
    if user_id:
        person = get_object_or_404(Person, id=user_id)

    if payment_id:
        payment = get_object_or_404(Payment, id=payment_id)
        form = PaymentForm(instance=payment)
        msg_log = "Payment modified."

    if request.method == 'POST':
        if payment_id:
            form = PaymentForm(request.POST, instance=payment)
        else:
            form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save()
            #LogEntry.objects.log_action(
            #    user_id = request.user.id,
            #    content_type_id = ContentType.objects.get_for_model(payment).pk,
            #    object_id = payment.pk, message = msg_log)
 
            messages.add_message(request, messages.SUCCESS,
                _('Payment has been successfully saved.'))
            return redirect(user_payments, user_id=payment.emitter.id)


    return render(request, 'payments/payment_edit.html', {
        'form': form, 'payment': payment,
        'back': request.META.get('HTTP_REFERER','/')})


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'])
@confirm_required(lambda payment_id=None :
    str(get_object_or_404(Payment, pk=payment_id)),
    'manage/base_manage.html',
    _('Do you really want to delete this payment'))
def payment_delete(request, payment_id=None):

    """delete a payment """

    payment = get_object_or_404(Payment, pk=payment_id)
    payment.delete()
    messages.add_message(request, messages.SUCCESS, _('Payment successfully deleted'))

    return redirect(payments)


def payment_distribute(request, payment_id=None):
    return

