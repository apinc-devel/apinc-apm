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

from django.db import models
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.contributions.models import Contribution
from apm.fields import PositiveNormalizedDecimalField 

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
    emitter = models.ForeignKey(Person, verbose_name=_('emitter'),
        related_name='payment')
    description = models.CharField(max_length=512, blank=False)
    amount = PositiveNormalizedDecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(verbose_name=_('payment date'))
    contributions = models.ManyToManyField(Contribution, null=True, blank=True, related_name='payments')

    
    def __unicode__(self):
        """unicode string for payment object"""
        return u'%s %s received on %s' % (self.emitter, self.description, self.date)

    class Meta:
        """Meta"""
        verbose_name = _('Payment')
        ordering = ['id']
