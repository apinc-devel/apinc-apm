# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Report.title'
        db.delete_column('association_report', 'title')


    def backwards(self, orm):
        
        # Adding field 'Report.title'
        db.add_column('association_report', 'title', self.gf('django.db.models.fields.CharField')(default='Title set by default', max_length=200), keep_default=False)


    models = {
        'association.report': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {}),
            'report_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'report_type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        }
    }

    complete_apps = ['association']
