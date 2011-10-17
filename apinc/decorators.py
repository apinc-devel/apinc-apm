# -*- coding: utf-8 -*-
"""
apinc/decorators.py
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
# Reading : http://gillesfabio.com/blog/2010/12/16/python-et-les-decorateurs/

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.utils.decorators import available_attrs


def access_required(view_func=None, groups=None, allow_myself=False):
    """
    Decorator for views that needs granted access.
    Applies the login_required decorator to the wrapped_view.

    groups       : is the list of groups to test the user membership against.
    allow_myself : requires that the decorated function be called with
                   'user_id' kwarg.
    """
    from django.conf import settings # ici limiter la visibilité des settings

    PERMISSION_DENIED_PAGE = 'auth/permission_denied.html'

    def decorator(view_func):
        """
        Decorator that checks if user belongs to groups
        """
        @wraps(view_func, assigned=available_attrs(view_func))
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            """
            Main decorator function that test user group membership against list
            of groups given as parameter.
            Redirect to a permission denied page if permissions are not granted.
            """
            from apinc.members.models import Person

            if not request.user:
                return render(request, PERMISSION_DENIED_PAGE, {})

            user = request.user 
            if not Person.objects.filter(user=user):
                return render(request, PERMISSION_DENIED_PAGE, {})

            user_groups = user.person.groups.values_list('group__name', flat=True)

            if allow_myself and kwargs.has_key('user_id'):
                if int(request.user.id) == int(kwargs['user_id']):
                    # Go to the decorated view
                    return view_func(request, *args, **kwargs)

            if settings.PORTAL_ADMIN in user_groups:
                # Go to the decorated view
                return view_func(request, *args, **kwargs)

            if not groups:
                return render(request, PERMISSION_DENIED_PAGE, {})

            for group in user_groups:
                if group in groups:
                    # Go to the decorated view
                    return view_func(request, *args, **kwargs)

            return render(request, PERMISSION_DENIED_PAGE, {})

        return _wrapped_view

    if view_func is None:
        # Decorator called with arguments
        def _dec(view_func):
            return decorator(view_func)
        return _dec

    # Decorator called without arguments
    return decorator(view_func)    

def confirm_required(get_description, section='base.html',
            message=_("Are you sure you want to do this action")):
    """
    Decorator for views that needs confirmation.
    """

    CONFIRM_KEY = "_confirm"
    CONFIRM_PAGE= "pages/confirm.html"

    def decorator(view_func):
        """
        Decorator that redirect to a simple form with a yes/no question.
        """
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            """
            Main decorator function for asking confirmation.
            """
            if request.method != 'POST' or not request.POST.has_key(CONFIRM_KEY):
                description = get_description(*args, **kwargs)
                back = request.META.get('HTTP_REFERER', '/')
                return render(request, CONFIRM_PAGE,
                    {'description': description, 'section': section,
                     'message': message, 'back': back})
            else:
                # Go to the decorated view
                return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
