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

import datetime

from django import forms
from django.utils.translation import ugettext as _

from apm.apps.pages.models import TextBlock
from tinymce.widgets import TinyMCE

class TextBlockForm(forms.ModelForm):
    """TextBlock generic form"""
    title = forms.CharField(label=_("title").capitalize(), max_length=150,
            required=True,widget=forms.TextInput(attrs={'size':'80'}))
    body_html = forms.CharField(label=_("body").capitalize(),
            max_length=100000000, required=False, widget=TinyMCE(attrs={'col':80, 'rows': 30}))

    class Meta:
        """TextBlock form meta"""
        model = TextBlock
        exclude = ('slug')

    # TODO validators
