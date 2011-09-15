# -*- coding: utf-8 -*-
"""
apinc/pages/views.py
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

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from apinc.pages.models import TextBlock
from apinc.pages.forms import TextBlockForm
from apinc.members.models import Person
from apinc.news.models import News
from apinc.decorators import access_required

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

@access_required(groups=['apinc-bureau', 'apinc-secretariat'])
def edit(request, page):
    """Edit pseudo-static generic text block"""

    text = get_object_or_404(TextBlock, slug=page)

    form = TextBlockForm(initial={'slug': text.slug, 'title': text.title,
        'body_html': text.body_html})

    if request.method == 'POST':
        form = TextBlockForm(request.POST)
        if form.is_valid():
            text.title = form.cleaned_data['title']
            text.body_html = form.cleaned_data['body_html']
            text.save()

            request.user.message_set.create(
                    message= _("Text %s page update." % page))

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
#FIXME login by email address
#    from django.db.models import Q

    next_page = request.GET.get('next','/')
    if not next_page == "":
        next_page = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        try:
            login = request.POST['username']
#            username = User.objects.filter(Q(person__user__email=login) | \
#                Q(username=login)).distinct().get().username
            password = request.POST['password']
#            user = auth.authenticate(username=username, password=password)
            user = auth.authenticate(username=login, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(request.POST.get('next','/'))
        except Exception:
           pass
        return render(request, 'auth/login.html',
            {'error': True, 'next': next_page})
    else:
        return render(request, 'auth/login.html',
            {'error': False, 'next': next_page})

