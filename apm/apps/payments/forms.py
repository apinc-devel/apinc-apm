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

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model as Person

from apm.apps.payments.models import Payment
from apm.apps.contributions.models import Contribution

class PaymentForm(forms.ModelForm):

    """Payment Form"""

    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder':_("Payment date")}))

    def __init__(self, *args, **kwargs):
        emitter_id = kwargs.pop('emitter_id', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields['contributions'].queryset = Contribution.objects.not_validated()

        payment = kwargs.get('instance', None)
        if payment:
            self.fields['contributions'].queryset = self.fields['contributions'].queryset | payment.contributions.all()

        if emitter_id:
            self.fields['emitter'].queryset = Person().objects.filter(id=emitter_id)

    def clean_contributions(self):
        data = self.cleaned_data['contributions']
        amount = self.cleaned_data.get('amount', None)
        if not amount:
            return data

        covered_amount = 0
        for c in data:
            covered_amount += c.dues_amount
        if covered_amount > amount:
            raise forms.ValidationError(_("Invalid amount against selected contributions"), code='invalid')

        return data

    class Meta:
        """Payment meta"""
        model = Payment
