# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Production'
        db.delete_table(u'bsee_loader_production')


    def backwards(self, orm):
        # Adding model 'Production'
        db.create_table(u'bsee_loader_production', (
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('production_oil', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('production_gas', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'bsee_loader', ['Production'])


    models = {
        
    }

    complete_apps = ['bsee_loader']