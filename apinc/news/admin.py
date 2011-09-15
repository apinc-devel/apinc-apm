# -*- coding: utf-8
"""
apinc/news/admin.py
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

from django.contrib import admin
from apinc.news.models import News

class NewsAdmin(admin.ModelAdmin):
      list_display = ('title', 'pub_date', 'status')
      search_fields = ['title', 'body_html']
      list_filter = ('pub_date', 'status')
      prepopulated_fields = {"slug" : ('title',)}
      fieldsets = (
          (None, {'fields': (('title', 'status'), 'body_html', 
                             ('pub_date', 'slug'))}),
      )

      class Media:
        js = ('/site_media/jquery/jquery-1.5.2.min.js',
              '/site_media/wymeditor/jquery.wymeditor.js',
              '/site_media/js/admin_textarea.js')
 
admin.site.register(News, NewsAdmin)
