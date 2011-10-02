# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Report.pub_date'
        db.alter_column('association_report', 'pub_date', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Changing field 'Report.pub_date'
        db.alter_column('association_report', 'pub_date', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'association.report': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {}),
            'report_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'report_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['association']
