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

from django import forms
from django.utils.translation import ugettext as _

from apm.apps.contributions.models import Contribution, ContributionType
from apm.apps.members.models import Person

class ContributionForm(forms.ModelForm):
    """Contribution form"""

    def __init__(self, *args, **kwargs):
        person_id = kwargs.pop('person_id', None)
        super(ContributionForm, self).__init__(*args, **kwargs)

        self.fields['type'].queryset = ContributionType.objects.active()
        self.fields['type'].empty_label = _('-- Select contribution type --')

        if person_id:
            self.fields['person'].queryset = Person.objects.filter(id=person_id)

    def clean_dues_amount(self):
        dues_amount = self.cleaned_data['dues_amount']

        if dues_amount <= 0:
            raise forms.ValidationError(_('Introduce a strictly positive number.'))

        return self.cleaned_data['dues_amount']

    class Meta:
        """ContributionForm meta"""
        model = Contribution
        exclude = ('validated', 'subscription_end_date', 
                   'subscription_start_date', 'recorded_date')


class ContributionTypeForm(forms.ModelForm):
    """Contribution Type Form"""

    class Meta:
        """ContributionType meta"""
        model = ContributionType
