# -*- coding: utf-8
"""
apinc/groups/models.py
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

from django.db import models
from django.utils.translation import ugettext as _

from apinc.members.models import Person

class GroupMembership(models.Model):
    """Store a person membership to a group"""

    group = models.ForeignKey('groups.Group', verbose_name=_('group'),
        related_name='members')
    member = models.ForeignKey('members.Person', verbose_name=_('member'),
        related_name='groups')

    start_date = models.DateField(verbose_name=_('start date'),
        default=datetime.date.today(), blank=True, null=True)
    end_date = models.DateField(verbose_name=_('end date'), blank=True,
        null=True)
    expiration_date = models.DateField(verbose_name=_('expiration date'),
        blank=True, null=True)


class Group(models.Model):
    slug = models.SlugField(verbose_name=_('slug'), max_length=50,
        unique=True)
    name = models.CharField(verbose_name=_('name'), max_length=100)
    about = models.TextField(verbose_name=_('description'), blank=True,
        null=True)

    email = models.EmailField(verbose_name=_('email'), max_length=50,
         blank=True, null=True)
#FIXME
#    icon = models.ImageField(verbose_name=_('icon'), upload_to='data/',
#         blank=True, null=True)

    class Meta:
        ordering = ['name', 'slug']

    def __unicode__(self):
        return self.name

    def has_for_member(self, person):
        """group membership test"""
        return self.members.filter(member=person)\
            .exclude(end_date__isnull=False,\
            end_date__lte=datetime.datetime.now())\
            .filter(start_date__lte=datetime.datetime.now())\
            .count() != 0

    def active_members(self):
        """current group members"""
        from django.db.models import Q
        return [ ms.member for ms in self.members.filter(Q(start_date__lte=\
            datetime.date.today()), Q(end_date__gte=datetime.date.today()) \
            | Q(end_date__isnull=True)) ]

    def all_members(self): #FIXME
        """all group members"""
        from django.db.models import Q
        return [ ms for ms in self.members.all() ]

    def add(self, person): #FIXME
        member = GroupMembership()
        member.group = self
        member.member = person
        member.start_date = datetime.date.today()
        member.save()

    def remove(self, person): #FIXME
        member = GroupMembership.objects.get(group=self, member=person)
        member.end_date = datetime.date.today()
        member.save()
