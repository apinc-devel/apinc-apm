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
