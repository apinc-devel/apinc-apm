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

from apinc.utils import CONFIDENTIALITY_LEVELS, portal_website_confidential

class Role(models.Model):
    
    name =  models.CharField(verbose_name=_('name'), max_length=100)
    rank = models.IntegerField(verbose_name=_('default rank'))

    def __unicode__(self):
        return self.name

    #def all_members(self): #FIXME
    #    """all group members"""
    #    from django.db.models import Q
    #    return [ ms for ms in self.members.all() ]

    def add(self, member): #FIXME test unicite ?
        member_role = MemberRole()
        member_role.role = self
        member_role.member = member
        member_role.start_date = datetime.date.today()
        member_role.save()

    def remove(self, member): #FIXME test active_member ?
        member_role = memberRole.objects.get(role=self, member=member)
        member_role.end_date = datetime.date.today()
        member_role.save()
  
class MemberRoleManager(models.Manager):
    def get_active_members(self):
        from django.db.models import Q
        return self.filter(
            Q(start_date__lte=datetime.date.today()),
            (Q(end_date__gte=datetime.date.today()) | 
            Q(end_date__isnull=True)))

class MemberRole(models.Model):
    """Store a role acted by a member"""

    role = models.ForeignKey('Role', verbose_name=_('role'),
        related_name='members')
    member = models.ForeignKey('Member', verbose_name=_('member'),
        related_name='roles')

    start_date = models.DateField(verbose_name=_('start date'),
        default=datetime.date.today(), blank=True, null=True)
    end_date = models.DateField(verbose_name=_('end date'), blank=True,
        null=True)
    expiration_date = models.DateField(verbose_name=_('expiration date'),
        blank=True, null=True)

    objects = MemberRoleManager()

    def __unicode__(self):
        return "Role '%s' : Member '%s'" % (unicode(self.role), unicode(self.member))  

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
        return unicode(self.get_full_name())

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
        """Person Private meta"""
        verbose_name = _('Person Private Data')
        ordering = ['person']

class Member(models.Model):
    """Member"""
    person = models.OneToOneField('Person', verbose_name=_('person'))

    def __unicode__(self):
        return unicode(self.person)

    class Meta:
        """Member meta"""
        ordering = ['person']

class Country(models.Model):
    """ Country (used for adresses)"""

    name = models.CharField(verbose_name=_('name'), max_length=50)
    nationality = models.CharField(verbose_name=_('nationality'), max_length=50)

    def __unicode__(self):
        """country unicode"""
        return unicode(self.name)

    class Meta:
        """country meta"""
        verbose_name = _('country')
        verbose_name_plural = _('country')

class Address(models.Model):
    """address of a person"""

    ADDRESS_TYPE = (
        (0, _('Personal')),
        (1, _('Business')),
        )

    person = models.ForeignKey(Person, related_name='addresses', editable=False)

    line1 = models.CharField(verbose_name=_('address line1'), max_length=50)
    line2 = models.CharField(verbose_name=_('address line2'), max_length=100,
        blank=True, null=True)
    zip_code = models.CharField(verbose_name=_('zip code'), max_length=20)
    city = models.CharField(verbose_name=_('city'), max_length=50)
    country = models.ForeignKey(Country, verbose_name=_('country'))
    type = models.IntegerField(verbose_name=_('adress type'),
        choices=ADDRESS_TYPE, default=0)
    confidentiality = models.IntegerField(verbose_name=_('confidentiality'),
        choices=CONFIDENTIALITY_LEVELS, default=0)

    def adr_type(self):
        return self.ADDRESS_TYPE[self.type][1]

    def website_confidential(self):
        """address confidentiality"""
        return portal_website_confidential(self)

    def confidentiality_print(self):
        """address confidentiality print"""
        print self.confidentiality
        return CONFIDENTIALITY_LEVELS[self.confidentiality][1]

    def __unicode__(self):
        """address unicode"""
        addr = self.line1
        if self.line2:
            addr += self.line2 + " - "
        else:
            addr += " - "
        addr += self.zip_code + " " + self.city + " - "
        addr += self.country.name
        return unicode(addr)

    class Meta:
        """address meta"""
        verbose_name = _('Address')

