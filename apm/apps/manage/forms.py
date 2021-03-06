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

from apm.apps.manage.models import GroupMembership

class GroupMembershipForm(forms.ModelForm):

    """GroupMembership Form"""

    def __init__(self, *args, **kwargs):
        member_id = kwargs.pop('member_id', None)
        super(GroupMembershipForm, self).__init__(*args, **kwargs)

        self.fields['group'].empty_label = _('-- Select apm group --')

        if member_id:
            self.fields['member'].queryset = Person().objects.filter(id=member_id)

    class Meta:
        """GroupMembership meta"""
        model = GroupMembership
