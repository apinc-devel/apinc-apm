# -*- coding: utf-8
"""
apinc/members/forms.py
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

import datetime

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from apinc.members.models import Person, PersonPrivate

class UserForm(forms.ModelForm):
    """User form"""
    class Meta:
        """User form meta"""
        model = User
#        exclude = ('id', 'username', 'password', 'is_staff', 'is_active',
#                   'is_superuser', 'last_login', 'date_joined')
        fields = ('last_name', 'first_name', 'email')

class PersonForm(forms.ModelForm):
    """Person form"""
    sex = forms.CharField(label=_("Gender").capitalize(),
            required=True,widget=forms.Select(choices=Person.SEX))
    birth_date = forms.DateField(label=_("birth date"), required=False)

    class Meta:
        """Person form meta"""
        model = Person
        exclude = ('user',)

class PersonPrivateForm(forms.ModelForm):
    """PersonPrivate form"""
    class Meta:
        """PersonPrivate form meta"""
        model = PersonPrivate
        exclude = ('person',)
