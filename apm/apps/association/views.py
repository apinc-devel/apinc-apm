# -*- coding: utf-8 -*-
#
#   Copyright © 2011-2013 APINC Devel Team
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

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.contrib import messages

from apm.apps.members.models import Person, MemberRole
from apm.apps.association.forms import ReportForm
from apm.apps.association.models import Report
from apm.apps.pages.models import TextBlock
from apm.decorators import access_required, confirm_required

def index(request):
    text = TextBlock.objects.get(slug='organization')
    board_members = MemberRole.objects.get_active_members().order_by('role__rank')
    meeting_reports = Report.objects.all()

    return render(request, 'association/index.html',
            {'text': text, 'board_members': board_members,
             'meeting_reports': meeting_reports})
    
def board(request):
    board_members = MemberRole.objects.get_active_members().order_by('role__rank')

    return render(request, 'association/board.html', 
            { 'board_members': board_members })

def statutes_pdf(request):
    return render(request, 'base.html')

@access_required(groups=['apinc-secretariat', 'apinc-bureau'])
def upload_report(request):
    """ Uploads or edit an association meeting report"""
    form = ReportForm()
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Modifications on reports have been successfully saved.'))
            return HttpResponseRedirect(reverse(index))

    return render(request, 'association/upload_report.html', {
        'form': form,
        'back': request.META.get('HTTP_REFERER','/') })

@access_required(groups=['apinc-secretariat', 'apinc-bureau'])
@confirm_required(lambda report_id: str(get_object_or_404(Report, pk=report_id)),
        section='association/base_association.html',
        message=_('Do you really want to delete this report'))
def delete_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    report.delete()
    messages.add_message(request, messages.INFO, _('Reported successfully deleted'))
    return HttpResponseRedirect(reverse(index))
