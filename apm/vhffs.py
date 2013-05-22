# -*- coding: utf-8 -*-

import os
import urlparse
import requests
import crypt
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import BasePasswordHasher

from apm.apps.members.models import PersonPrivate

USER_REST_URL = '/api/user/'

### TODO check and raise ImproperlyConfigured

def _vhffs_rest_api_url(url):
    netloc = settings.VHFFS_REST_API_SERVER
    if settings.VHFFS_REST_API_PORT:
        netloc += ':' + settings.VHFFS_REST_API_PORT
        
    return urlparse.urlunparse((settings.VHFFS_REST_API_SCHEME,
                                    netloc, url, None, None, None))

def sync_user_from_vhffs_api(username):
    """
    Update user data (password (hash), email, last_name, first_name) or
    create user if it does not exist according to vhffs rest api answer.
    """
    try:
        r = requests.get(_vhffs_rest_api_url(
                                os.path.join(USER_REST_URL, username)),
                                timeout=settings.VHFFS_REST_API_TIMEOUT)
        if not r:
            # TODO log message
            return 

        vhffs_user = r.json()

        if vhffs_user.has_key('username'): #FIXME tester le code http retour plutot
            try:
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                u = User.objects.create(username=username)
                pp = PersonPrivate.objects.create(person=u)
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

    # except requests.exception.timeout as e:
    except requests.RequestException as e:
        # TODO log erreur ambigue lors de l'appel a le requete de l'api vhffs rest
        # l'api rest vhffs est indisponible => on utilise auth_user
        print "pass the requests api not available."
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
