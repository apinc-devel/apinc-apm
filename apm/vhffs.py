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

import os
import urlparse
import requests
import crypt
import string
import datetime

from django.conf import settings
from django.contrib.auth.hashers import BasePasswordHasher
from django.contrib.auth import get_user_model

from apm.apps.members.models import Project

USERS_REST_URL = '/api/users'
PROJECTS_REST_URL = '/api/projects'

### TODO check and raise ImproperlyConfigured

def _vhffs_rest_api_url(url):
    """Internal"""
    netloc = settings.VHFFS_REST_API_SERVER
    if settings.VHFFS_REST_API_PORT:
        netloc += ':' + settings.VHFFS_REST_API_PORT
        
    return urlparse.urlunparse((settings.VHFFS_REST_API_SCHEME,
                                    netloc, url, None, None, None))


def _set_user(vhffs_user):
    """Internal"""
    u = None
    try:
        u = get_user_model().objects.get(username=vhffs_user['username'])
    except get_user_model().DoesNotExist:
        u = get_user_model().objects.create(username=vhffs_user['username'])
    finally:
        u.set_password_hash("vhffs" + vhffs_user['passwd'])
        if vhffs_user['mail']:
            u.email=vhffs_user['mail']
        else:
            #raise error
            pass
        if vhffs_user['lastname']:
            u.last_name=vhffs_user['lastname']
        else:
            #raise error
            pass
        if vhffs_user['firstname']:
            u.first_name=vhffs_user['firstname']
        else:
            #raise error
            pass
        u.save()

        print "User %s up to date." % (u)


def _set_project(vhffs_project):
    """Internal"""

    p = None
    u = None
    try:
        u = get_user_model().objects.get(username=vhffs_project['owner'])
    except get_user_model().DoesNotExist:
        raise Exception("Error: Owner (%s) does not exist while creating "
                        "project %s" % (vhffs_project['owner'], vhffs_project['groupname']))
    try:
        p = Project.objects.get(groupname=vhffs_project['groupname'])
    except Project.DoesNotExist:
        p = Project()
        p.groupname = vhffs_project['groupname']
    finally:
        p.owner = u
        p.creation_date = datetime.datetime.fromtimestamp(int(vhffs_project['creation_date']))
        p.save()

        print "Project %s up to date." % (p)


def sync_user_from_vhffs_api(username):
    """
    Update user data (password (hash), email, last_name, first_name) or
    create user if it does not exist according to vhffs rest api answer.  
    """
    try:
        r = requests.get(_vhffs_rest_api_url(
                                os.path.join(USERS_REST_URL, username)),
                                timeout=settings.VHFFS_REST_API_TIMEOUT)
        if not r:
            # TODO log message
            return 

        vhffs_user = r.json()

        if vhffs_user.has_key('username'): #FIXME tester le code http retour plutot
            _set_user(vhffs_user)

    # except requests.exception.timeout as e:
    except requests.RequestException as e:
        # TODO log erreur ambigue lors de l'appel a le requete de l'api vhffs rest
        # l'api rest vhffs est indisponible => on utilise auth_user
        print "pass the requests api not available. %s" % e
        pass


def sync_users_from_vhffs_api():
    """
    Sync all users data (password (hash), email, last_name, first_name) from
    vhffs database. Update data if user exists else create user.  
    """
    try:
        r = requests.get(_vhffs_rest_api_url(USERS_REST_URL), timeout=10)
        if not r:
            # TODO log message
            return 

        vhffs_users = r.json()

        for vu in vhffs_users:
            _set_user(vu)

    # except requests.exception.timeout as e:
    except requests.RequestException as e:
        # TODO log erreur ambigue lors de l'appel a le requete de l'api vhffs rest
        # l'api rest vhffs est indisponible => on utilise auth_user
        print "pass the requests api not available. %s" % e
        pass


def sync_projects_from_vhffs_api():
    """
    Sync all projects (groupname(project), owner(username) and creation date) from
    vhffs database. Update data if project exists else create project.  
    """
    try:
        r = requests.get(_vhffs_rest_api_url(PROJECTS_REST_URL), timeout=10)
        if not r:
            # TODO log message
            return 

        vhffs_projects = r.json()

        for vp in vhffs_projects:
            _set_project(vp)

    # except requests.exception.timeout as e:
    except requests.RequestException as e:
        # TODO log erreur ambigue lors de l'appel a le requete de l'api vhffs rest
        # l'api rest vhffs est indisponible => on utilise auth_user
        print "pass the requests api not available. %s" % e
        pass


class VhffsPasswordHasher(BasePasswordHasher):
    """
    The vhffs method of encoding, verifying passwords before r2126,
    before r2126 vhffs code uses Crypt::PasswdMD5
    Note, we only use the verify part of this PasswordHasher, the passwords
    are encoded with vhffs and synced via vhffs-rest-api
    """
    algorithm = "vhffs"
    salt_length = 8

    def salt(self):
        char_set = string.ascii_uppercase + string.digits
        salt = ''.join(random.sample(char_set, salt_length))
        salt = '$1$' + salt + '$'
        return salt

    def encode(self, password, salt):
        hashed = "%s%s" % (self.algorithm, crypt.crypt(str(password), salt))
        return hashed

    def verify(self, password, encoded):
        salt, hash = encoded[5:].rsplit("$", 1)
        return encoded == self.encode(password, salt)

#  local_tz = pytz.timezone("Europe/Paris")
#  local_dt = local_tz.normalize(datetime.datetime.utcfromtimestamp(float('1336579459')).replace(tzinfo=pytz.utc).astimezone(local_tz))

