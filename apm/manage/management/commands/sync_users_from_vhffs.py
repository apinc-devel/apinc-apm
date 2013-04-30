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

import requests

from django.core.management.base import NoArgsCommand, CommandError

import apm.apps.members.models as members
from apm.utils import vhffs_rest_api_url

USERS_REST_URL = "/api/users/"

class Command(NoArgsCommand):
    help = 'Sync django auth_users table from vhffs_users table using vhffs-rest-api.'

    def handle_noargs(self, *args, **options):
        try:
            r = requests.get(vhffs_rest_api_url(USERS_REST_URL))
            users = r.json()

            for user in users:
                try:
                    members.Person.objects.get(username=user['username'])
                except members.Person.DoesNotExist:
                    u = members.Person(username=user['username'])
                    u.set_password(user['passwd'])
                    if user['mail']:
                        u.email=user['mail']
                    if user['lastname']:
                        u.last_name=user['lastname']
                    if user['firstname']:
                        u.first_name=user['firstname']
                    u.is_staff = False
                    u.is_active = True
                    u.is_superuser = False
                    u.save()

                    self.stdout.write('User : %s inserted.\n' % (u.username))
                
            self.stdout.write('Done !\n')

            # Person
            #laurent = members.Person(username="laurent", email="lau@a.org",
            #        first_name="Laurent", last_name="Bives", sex="M",
            #        is_staff=True, is_superuser=True)
            #laurent.birth_date = date(1988,03,20)
            #laurent.set_password("laurent")
            #laurent.save()


        except Exception, e:
            # TODO Error message handling
            raise CommandError('sync_users_from_vhffs "%s"' % e)
