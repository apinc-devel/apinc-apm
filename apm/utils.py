import os
import urlparse
import requests

from django.conf import settings
from django.contrib.auth.models import User
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
                u.set_password(vhffs_user['passwd'])
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
