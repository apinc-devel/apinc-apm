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

import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _


def _get_sentinel_user():
    """Intermediate function in order to avoid direct call
    to get_user_model inside models.SET (was source of circular import)"""
    return get_user_model().objects.get_sentinel_user()

class LogEntryManager(models.Manager):
    def log_action(self, user_id, content_type_id, object_id, message=''):
        e = self.model(None, None, user_id, content_type_id, object_id,
                message[:255])
        e.save()

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
             on_delete=models.SET(_get_sentinel_user))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    logged_object = generic.GenericForeignKey('content_type', 'object_id')
    message = models.CharField(max_length=255, blank=True)

    objects = LogEntryManager()

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-timestamp',)

    def __unicode__(self):
        return "%s %s %s" % (self.timestamp, self.user, self.message)

    def get_edited_object(self):
        """Returns the edited object represented by this log entry"""
        return self.content_type.get_object_for_this_type(pk=self.object_id)


class Group(models.Model):
    """APM groups are used to handle permissions.
        They are not related to VHFFS groups (projects)"""
    slug = models.SlugField(verbose_name=_('slug'), max_length=50,
        unique=True)
    name = models.CharField(verbose_name=_('name'), max_length=100)
    about = models.TextField(verbose_name=_('description'), blank=True,
        null=True)

    email = models.EmailField(verbose_name=_('email'), max_length=50,
         blank=True, null=True)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMembership')

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
            .exclude(end_date__isnull=False,
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
        groupmembership = GroupMembership()
        groupmembership.group = self
        groupmembership.member = person
        groupmembership.start_date = datetime.date.today()
        groupmembership.save()

    def remove(self, person): #FIXME
        groupmembership = GroupMembership.objects.get(group=self, member=person)
        groupmembership.end_date = datetime.date.today()
        groupmembership.save()

class GroupMembership(models.Model):
    """Store a person membership to a group"""

    group = models.ForeignKey(Group)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('member'))

    start_date = models.DateField(verbose_name=_('start date'),
        default=datetime.date.today())
    end_date = models.DateField(verbose_name=_('end date'), blank=True,
        null=True)
    expiration_date = models.DateField(verbose_name=_('expiration date'),
        blank=True, null=True)

    class Meta:
        ordering = ['start_date', 'end_date', 'expiration_date', 'group__name']

    def __unicode__(self):
        return "Member '%s' : Group: '%s'" % (unicode(self.member),
                unicode(self.group))

