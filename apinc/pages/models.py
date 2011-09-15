# -*- coding: utf-8 -*-
"""
apinc/pages/models.py
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

from django.db import models
from django.utils.translation import ugettext as _

class TextBlock(models.Model):
    """Text Block"""

    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=16,
        unique=True,
        editable=False,
        help_text=_('Used for urls regex matches and templates <slug>.html.')
    )
    title = models.CharField(verbose_name=_("title"), max_length=200)
    body_html = models.TextField(blank=True)

    def __unicode__(self):
        """unicode string for text block"""
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('apinc.pages.views.page', { 'page': str(self.slug) })
