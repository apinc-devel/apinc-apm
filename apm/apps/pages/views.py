# -*- coding: utf-8 -*-
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

from django.contrib import auth, messages
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from apm.apps.members.models import Person
from apm.apps.pages.models import TextBlock
from apm.apps.pages.forms import TextBlockForm
from apm.apps.news.models import News
from apm.manage.models import LogEntry
from apm.decorators import access_required
from apm.vhffs import sync_user_from_vhffs_api

def homepage(request):
    """APINC homepage"""
    news = News.objects.filter(status__exact=1).order_by('-pub_date')[:5]

    text = TextBlock.objects.get(slug='homepage')

    return render(request, 'pages/homepage.html',
            {'news': news, 'text': text})

def page(request, page):
    """APINC pseudo-static generic page"""
    text = TextBlock.objects.get(slug=page)
    return render(request, 'pages/generic_page.html', { 'text': text })

@access_required(groups=['apinc-bureau', 'apinc-secretariat', 'apinc-contributeur'])
def edit(request, page):
    """Edit pseudo-static generic text block"""

    text = get_object_or_404(TextBlock, slug=page)

    form = TextBlockForm(instance=text)

    if request.method == 'POST':
        form = TextBlockForm(request.POST)
        if form.is_valid():
            text.title = form.cleaned_data['title']
            text.body_html = form.cleaned_data['body_html']
            text.save()

            msg_log = _("Pseudo-static page modified.")
            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id = ContentType.objects.get_for_model(text).pk,
                object_id = text.pk, message = msg_log)

            messages.add_message(request, messages.SUCCESS, _("Pseudo-static page '%s' updated." % page))

            return HttpResponseRedirect(reverse(page))

    return render(request, 'pages/text_edit.html',
            { 'text': text, 'form': form,
              'back':request.META.get('HTTP_REFERER') })

def logout(request):
    """logout page"""
    auth.logout(request)

    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('/')

def login(request):
    """login page"""
    from django.db.models import Q

    next_page = request.GET.get('next', '/')

    if request.method == 'POST':
        login = request.POST['username']

        try:
            login = request.POST['username']
            sync_user_from_vhffs_api(login)

            username = Person.objects.filter(Q(email=login) | \
                Q(username=login)).distinct().get().username
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return redirect(request.POST.get('next','/'))

        except Exception, e:
            #pass
            print "%s %s" % (e, e.__str__)
            # TODO traiter eventuelle erreur

        return render(request, 'auth/login.html',
            {'error': True, 'next': next_page})
    else:
        return render(request, 'auth/login.html',
            {'error': False, 'next': next_page})

def irc(request):
    """Irc iframe based on http://webirc.apinc.org"""
    return render(request, 'pages/irc.html')

