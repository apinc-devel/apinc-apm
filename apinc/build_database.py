#!/usr/bin/python
# -*- coding: utf-8
"""
apinc/build_database.py
"""
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
import pexpect
import sys

import settings

confirm = 'oui'

if os.path.exists(settings.DATABASES["default"]["NAME"]):
    msg = "La base de donnee existe deja, voulez vous la supprimer ? "
    confirm = raw_input(msg)
    while 1:
        if confirm not in ('oui', 'non'):
            confirm = raw_input('Merci de saisir "oui" ou "non" : ')
            continue
        if confirm == 'oui':
            os.remove(settings.DATABASES["default"]["NAME"])
        break

if confirm == 'non':
    sys.exit(0)

# -----------------------------------------------------------------------------
# spawn the child process
child = pexpect.spawn('python manage.py syncdb --noinput')

# log on stdout
child.logfile = sys.stdout

# This means wait for the end of the child's output
child.expect(pexpect.EOF, timeout=None)


# -----------------------------------------------------------------------------
# spawn the child process
child = pexpect.spawn('python manage.py migrate')

# log on stdout
child.logfile = sys.stdout

# This means wait for the end of the child's output
child.expect(pexpect.EOF, timeout=None)


# -----------------------------------------------------------------------------
msg = "Voulez-vous remplir la base de donnée avec des data de test ? "
confirm = raw_input(msg)
while 1:
    if confirm not in ('oui', 'non'):
        confirm = raw_input('Merci de saisir "oui" ou "non" : ')
        continue
    break

# spawn the child process
child = pexpect.spawn('python manage.py filldb')

# Wait for the application to give us this text (a regular expression)
child.expect("Voulez-vous remplir la base de donnée avec des data de test ? ")
# Send this line in response
child.sendline(confirm)

# log on stdout
child.logfile = sys.stdout

# This means wait for the end of the child's output
child.expect(pexpect.EOF, timeout=None)
