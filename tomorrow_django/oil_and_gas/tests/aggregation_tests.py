#
# Project: Tomorrow
#
# 07 February 2014
#
# Copyright 2014 by Lucas Fievet
# Salerstrasse 19, 8050 Zuerich
# All rights reserved.
#
# This software is the confidential and proprietary information
# of Lucas Fievet. ("Confidential Information"). You
# shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license
# agreement you entered into with Lucas Fievet.
#

from django.test import TestCase
from datetime import date

from ..models import FieldProduction, CountryProduction
from ..aggregation import CountryAggregator


class CountryAggregationTest(TestCase):
    field_production1, field_production2 = None, None
    field_production3, field_production4 = None, None
    field_production5 = None

    def setUp(self):
        self.field_production1 = FieldProduction.objects.create(
            name="NO-Field1",
            country="NO",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.field_production2 = FieldProduction.objects.create(
            name="NO-Field2",
            country="NO",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.field_production3 = FieldProduction.objects.create(
            name="UK-Field1",
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=1,
            production_gas=2,
            production_water=3,
        )
        self.field_production4 = FieldProduction.objects.create(
            name="UK-Field1",
            country="UK",
            date=date(year=1996, month=1, day=1),
            production_oil=4,
            production_gas=5,
            production_water=6,
        )
        self.field_production5 = FieldProduction.objects.create(
            name="UK-Field2",
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=10,
            production_gas=20,
            production_water=30,
        )
        self.field_production6 = FieldProduction.objects.create(
            name="UK-Field2",
            country="UK",
            date=date(year=1996, month=1, day=1),
            production_oil=100,
            production_gas=200,
            production_water=300,
        )

    def tearDown(self):
        self.field_production1.delete()
        self.field_production2.delete()
        self.field_production3.delete()
        self.field_production4.delete()
        self.field_production5.delete()

    def test_countries(self):
        """
        Tests get countries.
        """
        country_aggregator = CountryAggregator()
        countries = country_aggregator.get_countries()
        self.assertEqual(countries[0]['country'], self.field_production1.country)
        self.assertEqual(countries[1]['country'], self.field_production3.country)

    def test_aggregate_fields(self):
        """
        Tests aggregate single country.
        """
        country_aggregator = CountryAggregator()
        aggregate_fields = sorted(
            country_aggregator.aggregate_fields("UK"),
            key=lambda x: x['date']
        )
        expected = [{
            'date': date(1995, 1, 1),
            'total_oil': 11,
            'total_gas': 22,
            'total_water': 33
        }, {
            'date': date(1996, 1, 1),
            'total_oil': 104,
            'total_gas': 205,
            'total_water': 306
        }]
        self.assertDictEqual(aggregate_fields[0], expected[0])
        self.assertDictEqual(aggregate_fields[1], expected[1])

    def test_compute(self):
        """
        Tests compute aggregate wells for all fields.
        """
        country_aggregator = CountryAggregator()
        country_aggregator.compute()
        country_productions = sorted(
            CountryProduction.objects.filter(name="UK").all(),
            key=lambda x: x.date
        )
        self.assertEqual(country_productions[0].name, "UK")
        self.assertEqual(country_productions[0].date, date(1995, 1, 1))
        self.assertEqual(country_productions[0].production_oil, 11)
        self.assertEqual(country_productions[0].production_gas, 22)
        self.assertEqual(country_productions[0].production_water, 33)
        self.assertEqual(country_productions[1].name, "UK")
        self.assertEqual(country_productions[1].date, date(1996, 1, 1))
        self.assertEqual(country_productions[1].production_oil, 104)
        self.assertEqual(country_productions[1].production_gas, 205)
        self.assertEqual(country_productions[1].production_water, 306)
