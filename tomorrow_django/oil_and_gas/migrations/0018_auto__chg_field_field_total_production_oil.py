# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Field.total_production_oil'
        db.alter_column(u'oil_and_gas_field', 'total_production_oil', self.gf('django.db.models.fields.FloatField')())

    def backwards(self, orm):

        # Changing field 'Field.total_production_oil'
        db.alter_column(u'oil_and_gas_field', 'total_production_oil', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        u'oil_and_gas.country': {
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'current_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'current_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date_begin': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 14, 0, 0)'}),
            'discovery': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'error_avg': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'error_std': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'forecasts': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'future_dwarfs': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'future_giants': ('django.db.models.fields.TextField', [], {'default': "''"}),
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
            'total_production_oil': ('django.db.models.fields.FloatField', [], {'default': '0'}),
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
        u'oil_and_gas.discoveryscenario': {
            'Meta': {'object_name': 'DiscoveryScenario'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'discovery_scenarios'", 'null': 'True', 'blank': 'True', 'to': u"orm['oil_and_gas.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_dwarfs': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'number_giants': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pdf': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'probability': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'probability_dwarf': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'probability_giant': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'oil_and_gas.field': {
            'A': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'Meta': {'object_name': 'Field'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'beta': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'current_production_gas': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'current_production_oil': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date_begin': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 14, 0, 0)'}),
            'discovery': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'error_avg': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'error_std': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
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
            'total_production_oil': ('django.db.models.fields.FloatField', [], {'default': '0'}),
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
            'date_begin': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 14, 0, 0)'}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 14, 0, 0)'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'fits'", 'null': 'True', 'to': u"orm['oil_and_gas.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'r_squared': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sum_error': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tau': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'x_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['oil_and_gas']