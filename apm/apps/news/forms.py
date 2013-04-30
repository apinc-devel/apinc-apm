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

from apm.apps.news.models import News
from tinymce.widgets import TinyMCE


class NewsForm(forms.ModelForm):
    """News form"""
    title = forms.CharField(label=_("title").capitalize(), max_length=100,
            required=True,widget=forms.TextInput(attrs={'size':'50'}))
    body_html = forms.CharField(label=_("body").capitalize(),
            max_length=100000000, required=True, widget=TinyMCE(attrs={'cols': 80, 'rows': 24}))
    pub_date = forms.DateTimeField(label=_("publication date"),
            initial=datetime.datetime.today, required=True)

    class Meta:
        """News form meta"""
        model = News
        exclude = ('slug')

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save event"""
        news = super(NewsForm, self).save()
        return news
