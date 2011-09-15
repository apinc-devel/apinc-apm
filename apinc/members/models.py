# -*- coding: utf-8
"""
 apinc/members/models.py
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

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Role(models.Model):
    
    name =  models.CharField(verbose_name=_('name'), max_length=100)
    rank = models.IntegerField(verbose_name=_('default rank'))

    def __unicode__(self):
        return self.name
   
class PersonRole(models.Model):
    """Store a role acted by a person"""

    role = models.ForeignKey('Role', verbose_name=_('role'),
        related_name='members')
    person = models.ForeignKey('Person', verbose_name=_('person'),
        related_name='roles')

    start_date = models.DateField(verbose_name=_('start date'),
        default=datetime.date.today(), blank=True, null=True)
    end_date = models.DateField(verbose_name=_('end date'), blank=True,
        null=True)
    expiration_date = models.DateField(verbose_name=_('expiration date'), blank=True,
        null=True)


class Person(models.Model):
    """The main class for a person"""

    SEX = (
           ('M', _('Male')),
           ('F', _('Female')),
           )

    # User inheritance
    user = models.OneToOneField(User, verbose_name=_('user'))

    # Civility
    maiden_name = models.CharField(verbose_name=_('maiden name'),
        max_length=100, blank=True, null=True)
    birth_date = models.DateField(verbose_name=_('Birth date'), blank=True,
        null=True)
    sex = models.CharField(verbose_name=_('sex'), max_length=1, choices=SEX)
    #FIXME
    #country = models.ForeignKey(Country, verbose_name=_('nationality'),
    #    blank=True, null=True)

    def __unicode__(self):
        """person unicode"""
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('apinc.members.views.details', args=[self.id])

    class Meta:
        """person meta"""
        verbose_name = _('person')
        ordering = ['user__last_name', 'user__first_name']

    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name


class PersonPrivate(models.Model):
    """private data for a person"""

    person = models.OneToOneField(Person, verbose_name=_('person'))

    # Administration
    notes = models.TextField(verbose_name=_('Notes'), blank=True, null=True)

    def __unicode__(self):
        """Person private unicode"""
        return unicode(self.person)

    class Meta:
        """Person Private Data"""
        verbose_name = _('Person Private Data')
        ordering = ['person']

