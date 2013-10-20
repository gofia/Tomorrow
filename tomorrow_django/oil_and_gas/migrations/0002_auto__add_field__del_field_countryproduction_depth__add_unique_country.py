# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Field'
        db.create_table(u'oil_and_gas_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50)),
            ('production_oil', self.gf('django.db.models.fields.TextField')(default='')),
            ('production_gas', self.gf('django.db.models.fields.TextField')(default='')),
            ('production', self.gf('django.db.models.fields.TextField')(default='')),
            ('production_oil_smooth', self.gf('django.db.models.fields.TextField')(default='')),
            ('production_gas_smooth', self.gf('django.db.models.fields.TextField')(default='')),
            ('production_smooth', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'oil_and_gas', ['Field'])

        # Deleting field 'CountryProduction.depth'
        db.delete_column(u'oil_and_gas_countryproduction', 'depth')

        # Adding unique constraint on 'CountryProduction', fields ['date', 'name']
        db.create_unique(u'oil_and_gas_countryproduction', ['date', 'name'])

        # Adding unique constraint on 'FieldProduction', fields ['date', 'name']
        db.create_unique(u'oil_and_gas_fieldproduction', ['date', 'name'])

        # Adding unique constraint on 'WellProduction', fields ['date', 'name']
        db.create_unique(u'oil_and_gas_wellproduction', ['date', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'WellProduction', fields ['date', 'name']
        db.delete_unique(u'oil_and_gas_wellproduction', ['date', 'name'])

        # Removing unique constraint on 'FieldProduction', fields ['date', 'name']
        db.delete_unique(u'oil_and_gas_fieldproduction', ['date', 'name'])

        # Removing unique constraint on 'CountryProduction', fields ['date', 'name']
        db.delete_unique(u'oil_and_gas_countryproduction', ['date', 'name'])

        # Deleting model 'Field'
        db.delete_table(u'oil_and_gas_field')

        # Adding field 'CountryProduction.depth'
        db.add_column(u'oil_and_gas_countryproduction', 'depth',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    models = {
        u'oil_and_gas.countryproduction': {
            'Meta': {'unique_together': "(('name', 'date'),)", 'object_name': 'CountryProduction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'production_water': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'})
        },
        u'oil_and_gas.field': {
            'Meta': {'object_name': 'Field'},
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas_smooth': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil_smooth': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_smooth': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'oil_and_gas.fieldproduction': {
            'Meta': {'unique_together': "(('name', 'date'),)", 'object_name': 'FieldProduction'},
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
            'Meta': {'unique_together': "(('name', 'date'),)", 'object_name': 'WellProduction'},
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