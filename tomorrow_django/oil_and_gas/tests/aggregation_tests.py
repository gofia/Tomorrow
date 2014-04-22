__author__ = 'lucas.fievet'

from django.test import TestCase
from datetime import date

from oil_and_gas.models import FieldProduction, CountryProduction
from oil_and_gas.aggregation import CountryAggregator


class CountryAggregationTest(TestCase):
    fieldProduction1, fieldProduction2 = None, None
    fieldProduction3, fieldProduction4 = None, None
    fieldProduction5 = None

    def setUp(self):
        self.fieldProduction1 = FieldProduction.objects.create(
            name="NO-Field1",
            country="NO",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.fieldProduction2 = FieldProduction.objects.create(
            name="NO-Field2",
            country="NO",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.fieldProduction3 = FieldProduction.objects.create(
            name="UK-Field1",
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=1,
            production_gas=2,
            production_water=3,
        )
        self.fieldProduction4 = FieldProduction.objects.create(
            name="UK-Field1",
            country="UK",
            date=date(year=1996, month=1, day=1),
            production_oil=4,
            production_gas=5,
            production_water=6,
        )
        self.fieldProduction5 = FieldProduction.objects.create(
            name="UK-Field2",
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=10,
            production_gas=20,
            production_water=30,
        )
        self.fieldProduction6 = FieldProduction.objects.create(
            name="UK-Field2",
            country="UK",
            date=date(year=1996, month=1, day=1),
            production_oil=100,
            production_gas=200,
            production_water=300,
        )

    def tearDown(self):
        self.fieldProduction1.delete()
        self.fieldProduction2.delete()
        self.fieldProduction3.delete()
        self.fieldProduction4.delete()
        self.fieldProduction5.delete()

    def test_countries(self):
        """
        Tests get countries.
        """
        country_Aggregator = CountryAggregator()
        countries = country_Aggregator.getCountries()
        self.assertEqual(countries[0]['country'], self.fieldProduction1.country)
        self.assertEqual(countries[1]['country'], self.fieldProduction3.country)

    def test_aggregate_fields(self):
        """
        Tests aggregate single country.
        """
        country_Aggregator = CountryAggregator()
        aggregate_fields = country_Aggregator.aggregateFields("UK")
        expected = [{
            'date': date(1995, 1, 1),
            'total_gas': 11,
            'total_oil': 22,
            'total_water': 33
        }, {
            'date': date(1996, 1, 1),
            'total_gas': 104,
            'total_oil': 205,
            'total_water': 306
        }]
        self.assertDictEqual(aggregate_fields[0], expected[0])
        self.assertDictEqual(aggregate_fields[1], expected[1])

    def test_compute(self):
        """
        Tests compute aggregate wells for all fields.
        """
        country_Aggregator = CountryAggregator()
        country_Aggregator.compute()
        countryProductions = CountryProduction.objects.filter(name="UK").all()
        expected = [{
            'date': date(1995, 1, 1),
            'total_gas': 11,
            'total_oil': 22,
            'total_water': 33
        }, {
            'date': date(1996, 1, 1),
            'total_gas': 104,
            'total_oil': 205,
            'total_water': 306
        }]
        self.assertEqual(countryProductions[0].name, "UK")
        self.assertEqual(countryProductions[0].date, date(1995, 1, 1))
        self.assertEqual(countryProductions[0].production_gas, 11)
        self.assertEqual(countryProductions[0].production_oil, 22)
        self.assertEqual(countryProductions[0].production_water, 33)
        self.assertEqual(countryProductions[1].name, "UK")
        self.assertEqual(countryProductions[1].date, date(1996, 1, 1))
        self.assertEqual(countryProductions[1].production_gas, 104)
        self.assertEqual(countryProductions[1].production_oil, 205)
        self.assertEqual(countryProductions[1].production_water, 306)
