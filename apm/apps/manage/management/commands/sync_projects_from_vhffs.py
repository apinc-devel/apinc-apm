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

from django.core.management.base import NoArgsCommand, CommandError

from apm.vhffs import sync_projects_from_vhffs_api

class Command(NoArgsCommand):
    help = 'Sync django auth_users table from vhffs_users table using vhffs-rest-api.'

    def handle_noargs(self, *args, **options):
        try:
            sync_projects_from_vhffs_api()
        except Exception, e:
            # TODO Error message handling
            raise CommandError('sync_projects_from_vhffs "%s"' % e)
