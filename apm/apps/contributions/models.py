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

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.fields import PositiveNormalizedDecimalField


class ContributionTypeManager(models.Manager):
    def active(self):
        return self.filter(active__exact=True)

    def inactive(self):
        return self.filter(active__exact=False)


class ContributionType(models.Model):
    """
    The types of s are defined via the manage app interface.
    Two types are distinghuishable :
        . those who extend the subscription duration (annual subscription for instance)
        . those who do not extend the subscription duration (donation for instance)
    The management interface allows to define a label and if the type extends or not the subscription duration.
    """
    label = models.CharField(max_length=256, unique=True)
    extends_duration = models.PositiveIntegerField(default=None, blank=True, 
        null=True, verbose_name=_('duration (month)'))
    dues_amount = PositiveNormalizedDecimalField(max_digits=6, decimal_places=2,
        default=None, blank=True, null=True, verbose_name=_('dues amount'))
    active = models.BooleanField(verbose_name=_('active'), default=True)

    objects = ContributionTypeManager()

    def __unicode__(self):
        """unicode string for contribution type object"""
        return u'%s' % (self.label)

    class Meta:
        """Meta"""
        verbose_name = _('contribution type')
        ordering = ['-active', 'id']

#    CARD = 0
#    TRANSFER = 1
#    PAYPAL = 2
#    CHEQUE = 3
#    OTHER = 4
#
#    TENDER_TYPE = (
#                   (CARD, _('Card')),
#                   (TRANSFER, _('Transfer')),
#                   (PAYPAL, _('Paypal')),
#                   (CHEQUE, _('Cheque')),
#                   (OTHER, _('Other')),
#                   )

class Payment(models.Model):
    """
    A payment correspond to an overall payment for a member.

    A few data are required to create a payment :
        . a brief description,
        . the emitter,
        . the date (default to day date),
        . the amount

    Each payment it then shared out as contributions against payment amount.
    Consequently a payment has no incidence over a member subscription end date
    nor duration.
    """
    person = models.ForeignKey(Person, verbose_name=_('member'),
        related_name='payment')
    description = models.CharField(max_length=512, blank=False)
    amount = PositiveNormalizedDecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(verbose_name=_('payment date'),
        null=True, blank=True)
    
    def __unicode__(self):
        """unicode string for payment object"""
        return u'%s %s → %s' % (self.person, self.description, self.date)

    class Meta:
        """Meta"""
        verbose_name = _('Payment')
        ordering = ['id']


class ContributionManager(models.Manager):
    def validated(self):
        return self.filter(validated__exact=True)

    def order_subscriptions_for(self, person):
        subscriptions = list(self.filter(person=person)\
            .filter(type__extends_duration__gt=0).order_by('recorded_date'))
        first_subscription_date = person.get_first_subscription_date()

        print first_subscription_date
        if not first_subscription_date:
            # TODO log error
            return

        if len(subscriptions) < 1:
            return

        s1 = subscriptions.pop(0)
        if not s1.subscription_start_date == first_subscription_date:
            s1.subscription_start_date = first_subscription_date
            s1.subscription_end_date = s1.subscription_start_date \
                    + relativedelta(months=s1.type.extends_duration, days=-1)
            s1.save()
            
        if len(subscriptions) == 1:
            return

        for s2 in subscriptions:
            if s1.subscription_end_date != s2.subscription_start_date + relativedelta(days=-1):
                s2.subscription_start_date = s1.subscription_end_date + relativedelta(days=+1)
                s2.subscription_end_date = s2.subscription_start_date + relativedelta(months=+s2.type.extends_duration, days=-1)
                s2.save()
            s1 = s2
                    
        return


class Contribution(models.Model):

    """ A contribution corresponds to a subscription, a donation, a gift..."""

    person = models.ForeignKey(Person, verbose_name=_('person'),
        related_name='contribution')
    type = models.ForeignKey(ContributionType, verbose_name=_('contribution type'), 
        related_name='type', blank=False, null=False)
    payments = models.ManyToManyField('Payment', null=True, blank=True)
    dues_amount = PositiveNormalizedDecimalField(max_digits=6, decimal_places=2)
    validated = models.BooleanField(verbose_name=_('validated'), default=False)
    recorded_date = models.DateTimeField(verbose_name=_('record date'),
        auto_now_add=True)
    subscription_start_date = models.DateField(verbose_name=_('subscription start date'),
        null=True, blank=True)
    subscription_end_date = models.DateField(verbose_name=_('subscription end date'),
        null=True, blank=True)

    objects = ContributionManager()

    def __unicode__(self):
        """unicode string for contribution object"""
        return u'%s %s recorded on %s' % (self.type, self.person, self.recorded_date)

    class Meta:
        """Meta"""
        verbose_name = _('Contribution')
        ordering = ['-recorded_date']

    def delete(self):
        # FIXME payment obj
        #if self.payment:
        #    self.payment.delete()
        super(Contribution, self).delete()
        if self.type.extends_duration:
            Contribution.objects.order_subscriptions_for(self.person)
