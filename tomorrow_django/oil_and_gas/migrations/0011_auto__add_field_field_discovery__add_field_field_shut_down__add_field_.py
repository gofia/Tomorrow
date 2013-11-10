# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Field.discovery'
        db.add_column(u'oil_and_gas_field', 'discovery',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Field.shut_down'
        db.add_column(u'oil_and_gas_field', 'shut_down',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Field.current_production_oil'
        db.add_column(u'oil_and_gas_field', 'current_production_oil',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Field.current_production_gas'
        db.add_column(u'oil_and_gas_field', 'current_production_gas',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Field.stable'
        db.add_column(u'oil_and_gas_field', 'stable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Field.stable_since'
        db.add_column(u'oil_and_gas_field', 'stable_since',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.discovery'
        db.add_column(u'oil_and_gas_country', 'discovery',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.shut_down'
        db.add_column(u'oil_and_gas_country', 'shut_down',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.current_production_oil'
        db.add_column(u'oil_and_gas_country', 'current_production_oil',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Country.current_production_gas'
        db.add_column(u'oil_and_gas_country', 'current_production_gas',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Country.stable'
        db.add_column(u'oil_and_gas_country', 'stable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Country.stable_since'
        db.add_column(u'oil_and_gas_country', 'stable_since',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Field.discovery'
        db.delete_column(u'oil_and_gas_field', 'discovery')

        # Deleting field 'Field.shut_down'
        db.delete_column(u'oil_and_gas_field', 'shut_down')

        # Deleting field 'Field.current_production_oil'
        db.delete_column(u'oil_and_gas_field', 'current_production_oil')

        # Deleting field 'Field.current_production_gas'
        db.delete_column(u'oil_and_gas_field', 'current_production_gas')

        # Deleting field 'Field.stable'
        db.delete_column(u'oil_and_gas_field', 'stable')

        # Deleting field 'Field.stable_since'
        db.delete_column(u'oil_and_gas_field', 'stable_since')

        # Deleting field 'Country.discovery'
        db.delete_column(u'oil_and_gas_country', 'discovery')

        # Deleting field 'Country.shut_down'
        db.delete_column(u'oil_and_gas_country', 'shut_down')

        # Deleting field 'Country.current_production_oil'
        db.delete_column(u'oil_and_gas_country', 'current_production_oil')

        # Deleting field 'Country.current_production_gas'
        db.delete_column(u'oil_and_gas_country', 'current_production_gas')

        # Deleting field 'Country.stable'
        db.delete_column(u'oil_and_gas_country', 'stable')

        # Deleting field 'Country.stable_since'
        db.delete_column(u'oil_and_gas_country', 'stable_since')


    models = {
        u'oil_and_gas.country': {
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'current_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'current_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'discovery': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'shut_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stable_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'total_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'current_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'current_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'discovery': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'production': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_gas': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'production_oil': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'shut_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stable_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'total_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'date_begin': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 10, 0, 0)'}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 10, 0, 0)'}),
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