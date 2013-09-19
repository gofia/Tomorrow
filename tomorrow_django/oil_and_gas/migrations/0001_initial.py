# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CountryProduction'
        db.create_table(u'oil_and_gas_countryproduction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('production_oil', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('production_gas', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('production_water', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'oil_and_gas', ['CountryProduction'])

        # Adding model 'FieldProduction'
        db.create_table(u'oil_and_gas_fieldproduction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('production_oil', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('production_gas', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('production_water', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal(u'oil_and_gas', ['FieldProduction'])

        # Adding model 'WellProduction'
        db.create_table(u'oil_and_gas_wellproduction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('production_oil', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('production_gas', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('production_water', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('field', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal(u'oil_and_gas', ['WellProduction'])


    def backwards(self, orm):
        # Deleting model 'CountryProduction'
        db.delete_table(u'oil_and_gas_countryproduction')

        # Deleting model 'FieldProduction'
        db.delete_table(u'oil_and_gas_fieldproduction')

        # Deleting model 'WellProduction'
        db.delete_table(u'oil_and_gas_wellproduction')


    models = {
        u'oil_and_gas.countryproduction': {
            'Meta': {'object_name': 'CountryProduction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'production_water': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'})
        },
        u'oil_and_gas.fieldproduction': {
            'Meta': {'object_name': 'FieldProduction'},
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'production_water': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'})
        },
        u'oil_and_gas.wellproduction': {
            'Meta': {'object_name': 'WellProduction'},
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'production_water': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oil_and_gas']