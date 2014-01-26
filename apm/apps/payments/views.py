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

from paypalrestsdk import Payment as PaypalPayment

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.payments.models import Payment, PaypalMapping
from apm.apps.payments.forms import PaymentForm
from apm.decorators import access_required, confirm_required
from apm.apps.contributions.models import Contribution

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


@access_required(groups=['apinc-secretariat', 'apinc-tresorier'],
    allow_myself=True)
def payment_details(request, payment_id=None):

    """Display payment detailed content"""

    payment = get_object_or_404(Payment, id=payment_id)
    person = get_object_or_404(Person, id=payment.emitter.id)

    return render(request, 'payments/payment_details.html',
        {'person': person, 'payment': payment,
         'next' : request.GET.get('next', '/')})


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
        form = PaymentForm(instance=payment, emitter_id=user_id)
        msg_log = "Payment modified."

    if request.method == 'POST':
        #print request.POST.getlist('contributions')
        if payment_id:
            form = PaymentForm(request.POST, instance=payment, emitter_id=user_id)
        else:
            form = PaymentForm(request.POST, emitter_id=user_id)

        if form.is_valid():      
            contributions = form.cleaned_data['contributions']
            try:
                if form.instance:
                    for c in form.instance.contributions.all():
                        if c not in contributions:
                            c.validated = False
                            c.save()
            except:
                pass

            for c in contributions:
                c.validated = True
                c.save()

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

    return redirect(request.POST.get('next', reverse(payments)))


def pay(request, contribution_id=None):

    contribution = get_object_or_404(Contribution, id=contribution_id)
    return render(request, 'payments/pay.html',
        {'person': contribution.person, 'contribution': contribution,
         'next' : request.GET.get('next', '/')})


def paypal_create(request, contribution_id=None):
    
    contribution = get_object_or_404(Contribution, id=contribution_id)
    paypal_mapping = PaypalMapping()

    ### create paypal payment
    paypal_payment = PaypalPayment({
        "intent":  "sale",

        # ###Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer":  {
            "payment_method":  "paypal" },

        # ###Redirect URLs
        "redirect_urls": {
            "return_url": "%s?next=%s" % (request.build_absolute_uri(reverse(paypal_execute, kwargs={'contribution_id':contribution_id, 'uuid':paypal_mapping.uuid})), request.GET.get('next','/')),
            "cancel_url": "%s?next=%s" % (request.build_absolute_uri(reverse(paypal_cancel, kwargs={'uuid':paypal_mapping.uuid})), request.GET.get('next','/')) },

        # ###Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions":  [ {

        # ### ItemList
        "item_list": {
          "items": [{
            "name": contribution.type.label,
            "sku": paypal_mapping.uuid,
            "price": str(contribution.dues_amount),
            "currency": "EUR",
            "quantity": 1 }]},

        # ###Amount
        # Let's you specify a payment amount.
        "amount":  {
          "total":  str(contribution.dues_amount),
          "currency":  "EUR" },
        "description":  _("Contribution payment") + " %s." % contribution } ] } )

    # Create Payment and return status
    if paypal_payment.create():
        paypal_mapping.payment_id = paypal_payment.id 
        paypal_mapping.save()
        #print("Payment[%s] created successfully"%(paypal_payment.id))
        # Redirect the user to given approval url
        for link in paypal_payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                print("Redirect for approval: %s"%(redirect_url))
                return redirect(redirect_url)
    else:
        print("Error while creating payment:")
        print(paypal_payment.error)

    messages.add_message(request, messages.ERROR,
        _('An error occured while creating the payment, please contact administrators.'))
    return redirect(request.GET.get('next', '/'))

def paypal_execute(request, contribution_id=None, uuid=None):

    payer_id = request.GET.get('PayerID') 
    if not payer_id:
        messages.add_message(request, messages.ERROR,
            _('An error occured while processing the payment') + " %s " \
                % (paypal_mapping.payment_id) + _("PayerID not found."))
        return redirect(request.GET.get('next'))

    paypal_mapping = get_object_or_404(PaypalMapping, uuid=uuid)
    contribution = get_object_or_404(Contribution, id=contribution_id)
    paypal_payment = PaypalPayment.find(paypal_mapping.payment_id)

    if paypal_payment.execute({"payer_id": payer_id}):
        #print("Payment[%s] execute successfully"%(paypal_payment.id))
        payment = Payment(
                emitter=contribution.person,
                description = paypal_payment.id,
                amount = paypal_payment.transactions[0]['amount']['total'],
                date = datetime.datetime.now())
        payment.save()
        payment.contributions.add(contribution.id)

        contribution.validated = True
        contribution.save()
        return redirect(request.GET.get('next'))
    else:
        messages.add_message(request, messages.ERROR,
            _('An error occured while processing the payment') + " %s." \
                % paypal_mapping.payment_id)
        return redirect(request.GET.get('next'))
        print(paypal_payment.error)

def paypal_cancel(request, uuid=None):
    paypal_mapping = get_object_or_404(PaypalMapping, uuid=uuid)
    paypal_mapping.delete()
    messages.add_message(request, messages.WARNING, _('The payment ') + " %s " \
            % paypal_mapping.payment_id + _('has been cancelled'))
    return redirect(request.GET.get('next'))
