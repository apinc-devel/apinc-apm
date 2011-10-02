# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Report'
        db.create_table('association_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('report_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('report_type', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal('association', ['Report'])


    def backwards(self, orm):
        
        # Deleting model 'Report'
        db.delete_table('association_report')


    models = {
        'association.report': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'report_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'report_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['association']
