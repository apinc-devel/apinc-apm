# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TextBlock'
        db.create_table('pages_textblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=16, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pages', ['TextBlock'])


    def backwards(self, orm):
        
        # Deleting model 'TextBlock'
        db.delete_table('pages_textblock')


    models = {
        'pages.textblock': {
            'Meta': {'object_name': 'TextBlock'},
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '16', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pages']
