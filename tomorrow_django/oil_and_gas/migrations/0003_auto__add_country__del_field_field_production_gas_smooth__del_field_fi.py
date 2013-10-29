# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'oil_and_gas_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50)),
            ('production_oil', self.gf('django.db.models.fields.TextField')(default='')),
            ('production_gas', self.gf('django.db.models.fields.TextField')(default='')),
            ('production', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'oil_and_gas', ['Country'])

        # Deleting field 'Field.production_gas_smooth'
        db.delete_column(u'oil_and_gas_field', 'production_gas_smooth')

        # Deleting field 'Field.production_smooth'
        db.delete_column(u'oil_and_gas_field', 'production_smooth')

        # Deleting field 'Field.production_oil_smooth'
        db.delete_column(u'oil_and_gas_field', 'production_oil_smooth')

        # Adding field 'Field.A'
        db.add_column(u'oil_and_gas_field', 'A',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=20, decimal_places=10),
                      keep_default=False)

        # Adding field 'Field.tau'
        db.add_column(u'oil_and_gas_field', 'tau',
                      self.gf('django.db.models.fields.DecimalField')(default=-1.0, max_digits=20, decimal_places=10),
                      keep_default=False)

        # Adding field 'Field.beta'
        db.add_column(u'oil_and_gas_field', 'beta',
                      self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=20, decimal_places=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'oil_and_gas_country')

        # Adding field 'Field.production_gas_smooth'
        db.add_column(u'oil_and_gas_field', 'production_gas_smooth',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Field.production_smooth'
        db.add_column(u'oil_and_gas_field', 'production_smooth',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Field.production_oil_smooth'
        db.add_column(u'oil_and_gas_field', 'production_oil_smooth',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Field.A'
        db.delete_column(u'oil_and_gas_field', 'A')

        # Deleting field 'Field.tau'
        db.delete_column(u'oil_and_gas_field', 'tau')

        # Deleting field 'Field.beta'
        db.delete_column(u'oil_and_gas_field', 'beta')


    models = {
        u'oil_and_gas.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
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
            'A': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '10'}),
            'Meta': {'object_name': 'Field'},
            'beta': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '20', 'decimal_places': '10'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'tau': ('django.db.models.fields.DecimalField', [], {'default': '-1.0', 'max_digits': '20', 'decimal_places': '10'})
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