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
#

import decimal

from django.db.models import DecimalField, SubfieldBase
from django.core import exceptions
from django.utils.translation import ugettext as _

# idea taken from http://tothinkornottothink.com/post/2156476872/django-positivenormalizeddecimalfield

class PositiveNormalizedDecimalField(DecimalField):
    __metaclass__ = SubfieldBase

    default_error_messages = {
        'positive': _('Introduce a positive number.'),
    }

    def to_python(self, value):
        if value is None:
            return value
        try:
            # we want to return a normalized non-scientific notation decimal
            number = decimal.Decimal('{0:f}'.format(decimal.Decimal(str(value)).normalize()))

            # This ensures no negative number can get to the model (model validation)
            if number < decimal.Decimal(0):
                raise exceptions.ValidationError(self.error_messages['positive'])

            return number

        except decimal.InvalidOperation:
            raise exceptions.ValidationError(self.error_messages['invalid'])
