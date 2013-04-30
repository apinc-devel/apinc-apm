# -*- coding: utf-8 -*-
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

from django import forms
from django.utils.translation import ugettext as _

#from django.contrib.auth.models import User
from apm.apps.members.models import Person, PersonPrivate

class PersonForm(forms.ModelForm):
    """Person form"""
    class Meta:
        """Person form meta"""
#        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'sex', 'birth_date', 'maiden_name',)
        exclude = ('is_staff', 'is_active', 'password', 'date_joined', 'last_login',)

class PersonPrivateForm(forms.ModelForm):
    """PersonPrivate form"""
    class Meta:
        """PersonPrivate form meta"""
        model = PersonPrivate
        exclude = ('person',)
