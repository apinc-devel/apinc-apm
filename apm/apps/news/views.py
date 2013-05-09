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

import datetime

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apm.apps.news.models import News
from apm.apps.news.forms import NewsForm
from apm.manage.models import LogEntry
from apm.decorators import access_required, confirm_required

def index(request):
    """Published news index"""
    nb_news_per_page = 5 

    paginator = Paginator(News.objects.published(), nb_news_per_page)
    
    page = request.GET.get('page', 1) 
    try:
        news = paginator.page(page)
    except InvalidPage:
        raise Http404

    return render(request, 'news/index.html', {
        'news': news,
        'archives': _archives(),
        'got_draft': (News.objects.drafted().count() > 0)  })

@access_required(groups=['apinc-admin', 'apinc-secretariat', 'apinc-bureau'])
@confirm_required(lambda news_slug: str(get_object_or_404(News, slug=news_slug)),
        section='news/base_news.html',
        message=_('Do you really want to delete this news'))
def delete(request, news_slug):
    """News delete"""

    news_item = get_object_or_404(News, slug=news_slug)
    news_item.delete()

    messages.add_message(request, messages.SUCCESS, _('The news has been successfully deleted.'))
    #request.user.message_set.create(message=
    #   _('The news has been successfully deleted.'))
    return HttpResponseRedirect(reverse(index))

@access_required(groups=['apinc-secretariat', 'apinc-bureau',
                    'apinc-contributeur'])
def edit(request, news_slug=None):
    """News edit"""

    news_item = None
    form = NewsForm()
    msg_log = "News created."

    if news_slug:
        news_item = get_object_or_404(News, slug=news_slug)
        form = NewsForm(instance=news_item)
        msg_log = "News modified."

    if request.method == 'POST':
        if news_slug:
            form = NewsForm(request.POST, request.FILES, instance=news_item)
        else:
            form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            news_item = form.save()
            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id = ContentType.objects.get_for_model(news_item).pk,
                object_id = news_item.pk, message = msg_log)
 
            messages.add_message(request, messages.SUCCESS, _('Modifications have been successfully saved.'))
            if news_item.is_published():
                return HttpResponseRedirect(reverse(
                                      published_details, args=[news_item.slug]))
            else:
                return HttpResponseRedirect(reverse(
                                      draft_details, args=[news_item.slug]))

    return render(request, 'news/edit.html', {
        'form': form, 'news_item': news_item,
        'back': request.META.get('HTTP_REFERER','/'),
        'archives': _archives() })

def published_details(request, news_slug):
    """Published news details"""
    news_item = get_object_or_404(News, slug=news_slug)
    return render(request, 'news/published_details.html', {
        'news_item': news_item,
        'archives': _archives() })

def published(request, year=None, month=None, day=None):
    """Archives of published news"""
    nb_news_per_page = 5 

    if year:
        period = {'pub_date__year': year}
    else:
        period = {'pub_date__year': timezone.now().year}
    if month : period['pub_date__month'] = month
    if day : period['pub_date__day'] = day

    paginator = Paginator(News.objects.published(period=period), nb_news_per_page)
    
    page = request.GET.get('page', 1) 
    try:
        news = paginator.page(page)
    except InvalidPage:
        raise Http404

    return render(request, 'news/published.html', {
        'news': news,
        'archives': _archives() })

@access_required(groups=['apinc-secretariat', 'apinc-bureau',
                    'apinc-contributeur'])
def draft_details(request, news_slug):
    """Drafted news details"""
    news_item = get_object_or_404(News, slug=news_slug)
    return render(request, 'news/draft_details.html', {
        'news_item': news_item,
        'archives': _archives() })

@access_required(groups=['apinc-secretariat', 'apinc-bureau',
                    'apinc-contributeur'])
def drafts(request):
    """Index of drafted news"""
    nb_news_per_page = 5

    paginator = Paginator(News.objects.drafted(), nb_news_per_page)
    
    page = request.GET.get('page', 1)
    try:
        news = paginator.page(page)
    except InvalidPage:
        raise Http404
    
    return render(request, 'news/drafts.html', {
        'news': news,
        'archives': _archives() })

def _archives():
    """Returns a list of published news by date"""

    year_list = News.objects.published().dates('pub_date', 'year')[::-1]

    news_list = []
    for year in year_list:
        month_list = News.objects.published().filter(pub_date__year=year.year) \
                .dates('pub_date', 'month')[::-1]
        for month in month_list:
            lookup_kwargs = { 'pub_date__year': year.year,
                              'pub_date__month': month.month }
            news_list.append((datetime.datetime(year.year, month.month, 1),
                News.objects.published().filter(**lookup_kwargs).count()))
            ### FIXME : Voir billet du 01/04/2006 comptabilisé sur le mois de mars 2006.
            #import datetime
            #from django.utils.timezone import utc
            #now = datetime.datetime.utcnow().replace(tzinfo=utc)
            #news_list.append((datetime.datetime(year.year, month.month, 1, 0, 0, 0).replace(tzinfo=utc),
            #    News.objects.published().filter(**lookup_kwargs).count()))

    return news_list

