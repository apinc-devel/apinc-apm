# -*- coding: utf-8
"""
apinc/association/models.py
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

import os
import re

from django.db import models
from django.utils.translation import ugettext as _

MEETING_REPORT = 0
AG_REPORT = 1
CA_REPORT = 2

REPORT_PATH = 'reports'

def _update_filename(instance, filename):
    return os.path.join(REPORT_PATH, "%s_%s%s" % (
        re.sub(r' ', '_', instance.get_report_type_display().lower()),
        instance.pub_date.strftime("%B_%Y").lower(),
        os.path.splitext(filename)[1])) # filename extension

class Report(models.Model):
    report_file = models.FileField(upload_to=_update_filename)
    pub_date = models.DateField('Date published')
    REPORT_TYPE = (
        (MEETING_REPORT, _('Meeting Report')),
        (AG_REPORT, _('AG Report')),
        (CA_REPORT, _('CA Report')),
    )
    report_type = models.IntegerField(choices=REPORT_TYPE, default=CA_REPORT)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name_plural = 'reports'

    def __unicode__(self):
        return u'%s %s' % (self.get_report_type_display(),
                           self.pub_date.strftime("%B %Y"))

    def get_previous(self):
        return self.get_previous_by_pub_date()

    def get_next(self):
        return self.get_next_by_pub_date()

    def delete(self, *args, **kwargs):
        if self.report_file:
            self.report_file.delete()
        super(Report, self).delete(*args, **kwargs)
