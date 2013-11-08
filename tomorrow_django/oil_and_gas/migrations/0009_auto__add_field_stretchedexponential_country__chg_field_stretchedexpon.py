# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StretchedExponential.country'
        db.add_column(u'oil_and_gas_stretchedexponential', 'country',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='fits', null=True, blank=True, to=orm['oil_and_gas.Country']),
                      keep_default=False)


        # Changing field 'StretchedExponential.field'
        db.alter_column(u'oil_and_gas_stretchedexponential', 'field_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['oil_and_gas.Field']))
        # Adding field 'Country.x_min'
        db.add_column(u'oil_and_gas_country', 'x_min',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Country.A'
        db.add_column(u'oil_and_gas_country', 'A',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Country.tau'
        db.add_column(u'oil_and_gas_country', 'tau',
                      self.gf('django.db.models.fields.FloatField')(default=-1.0),
                      keep_default=False)

        # Adding field 'Country.beta'
        db.add_column(u'oil_and_gas_country', 'beta',
                      self.gf('django.db.models.fields.FloatField')(default=1.0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StretchedExponential.country'
        db.delete_column(u'oil_and_gas_stretchedexponential', 'country_id')


        # Changing field 'StretchedExponential.field'
        db.alter_column(u'oil_and_gas_stretchedexponential', 'field_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['oil_and_gas.Field']))
        # Deleting field 'Country.x_min'
        db.delete_column(u'oil_and_gas_country', 'x_min')

        # Deleting field 'Country.A'
        db.delete_column(u'oil_and_gas_country', 'A')

        # Deleting field 'Country.tau'
        db.delete_column(u'oil_and_gas_country', 'tau')

        # Deleting field 'Country.beta'
        db.delete_column(u'oil_and_gas_country', 'beta')


    models = {
        u'oil_and_gas.country': {
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'object_name': 'Country'},
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'x_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'object_name': 'Field'},
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'x_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
        u'oil_and_gas.stretchedexponential': {
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'unique_together': "(('field', 'date_begin', 'date_end'),)", 'object_name': 'StretchedExponential'},
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'fits'", 'null': 'True', 'blank': 'True', 'to': u"orm['oil_and_gas.Country']"}),
            'date_begin': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 7, 0, 0)'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'fits'", 'null': 'True', 'to': u"orm['oil_and_gas.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sum_error': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'x_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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