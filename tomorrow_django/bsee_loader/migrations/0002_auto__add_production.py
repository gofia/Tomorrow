# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Production'
        db.create_table(u'bsee_loader_production', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('production_oil', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('production_gas', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'bsee_loader', ['Production'])


    def backwards(self, orm):
        # Deleting model 'Production'
        db.delete_table(u'bsee_loader_production')


    models = {
        u'bsee_loader.production': {
            'Meta': {'object_name': 'Production'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['bsee_loader']