# -*- coding: utf-8 _*_
#
#   Copyright © 2013 Project Devel Team
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

from django import template
from apm.apps.contributions.models import Contribution

register = template.Library()

@register.filter
def is_selected_contribution(value, contributions):
    selected = ""
    for c in contributions:
        if c.id == value.id:
            selected = 'selected="selected"'
            break
    return selected
