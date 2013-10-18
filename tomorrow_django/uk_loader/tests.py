"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.utils import override_settings
from datetime import date
from BeautifulSoup import BeautifulSoup

from oil_and_gas.models import WellProduction, FieldProduction
from uk_loader.models import UkRequest, UkManager, UkAggregator
from uk_loader.tasks import updateUk

class UkRequestTest(TestCase):
    def test_get_production(self):
        """
        Tests that production is correct.
        """
        soup = BeautifulSoup('<tr><td align="RIGHT" height="15"><font face="Arial" size="1">1995</font>' +
                             '</td><td align="RIGHT"><font face="Arial" size="1">1</font></td><td align="RIGHT">' +
                             '<font face="Arial" size="1">46,742</font></td><td align="RIGHT">' +
                             '<font face="Arial" size="1">2,184</font></td><td align="RIGHT">' +
                             '<font face="Arial" size="1">1,035</font></td><td align="RIGHT">' +
                             '<font face="Arial" size="1">13.20</font></td><td align="RIGHT">' +
                             '<font face="Arial" size="1">17.33</font></td></tr>')
        ukRequest = UkRequest()
        production = ukRequest.getProduction(soup)
        expectedProduction = WellProduction(
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.production_water, expectedProduction.production_water)

    def test_get_soup(self):
        """
        Tests that production is correct.
        """
        ukRequest = UkRequest()
        soup = ukRequest.getSoup(page=0)
        table = soup.find('table', width=490, border=1)
        trs = table.findAll('tr')
        self.assertEqual(len(trs), 61)

    def test_get_production_page(self):
        """
        Tests that production is correct.
        """
        ukRequest = UkRequest()
        productions = ukRequest.getProductionPage(0)
        self.assertEqual(len(productions), 60)
        production = productions[0]
        expectedProduction = WellProduction(
            name="16/26-A11",
            field="Alba",
            country="UK",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.field, expectedProduction.field)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.production_water, expectedProduction.production_water)
        production = productions[-1]
        expectedProduction = WellProduction(
            name="16/26-A11",
            field="Alba",
            country="UK",
            date=date(year=1999, month=12, day=1),
            production_oil=0,
            production_gas=0,
            production_water=0,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.field, expectedProduction.field)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.production_water, expectedProduction.production_water)


class UkManagerTest(TestCase):
    def test_update(self):
        """
        Tests update.
        """
        ukManager = UkManager()
        self.assertEqual(ukManager.getYoungestDate(0), date(year=1947, month=11, day=1))
        ukManager.update(1)
        count = WellProduction.objects.count()
        self.assertEqual(count, 88)
        self.assertEqual(ukManager.getYoungestDate("16/26-A11"), date(year=1999, month=12, day=1))

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def test_async_update(self):
        result = updateUk.delay(2)
        self.assertEquals(result.get(), 141)
        self.assertTrue(result.successful())


class UkAggregatorTest(TestCase):
    wellProduction1, wellProduction2 = None, None

    def setUp(self):
        self.wellProduction1 = WellProduction.objects.create(
            name="Well1",
            country="UK",
            field="Field1",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        self.wellProduction2 = WellProduction.objects.create(
            name="Well1",
            country="UK",
            field="Field2",
            date=date(year=1995, month=1, day=1),
            production_oil=46742,
            production_gas=2184,
            production_water=1035,
        )
        wellProduction1_1 = WellProduction.objects.create(
            name="Well1",
            country="UK",
            field="Field3",
            date=date(year=1995, month=1, day=1),
            production_oil=1,
            production_gas=2,
            production_water=3,
        )
        wellProduction1_2 = WellProduction.objects.create(
            name="Well1",
            country="UK",
            field="Field3",
            date=date(year=1996, month=1, day=1),
            production_oil=4,
            production_gas=5,
            production_water=6,
        )
        wellProduction2_1 = WellProduction.objects.create(
            name="Well2",
            country="UK",
            field="Field3",
            date=date(year=1995, month=1, day=1),
            production_oil=10,
            production_gas=20,
            production_water=30,
        )
        wellProduction2_2 = WellProduction.objects.create(
            name="Well2",
            country="UK",
            field="Field3",
            date=date(year=1996, month=1, day=1),
            production_oil=100,
            production_gas=200,
            production_water=300,
        )

    def test_fields(self):
        """
        Tests get fields.
        """
        ukAggregator = UkAggregator()
        fields = ukAggregator.getFields()
        self.assertEqual(fields[0]['field'], self.wellProduction1.field)
        self.assertEqual(fields[1]['field'], self.wellProduction2.field)

    def test_aggregate_wells(self):
        """
        Tests aggregate single field.
        """
        ukAggregator = UkAggregator()
        aggregate_wells = ukAggregator.aggregateWells("Field3")
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
        self.assertDictEqual(aggregate_wells[0], expected[0])
        self.assertDictEqual(aggregate_wells[1], expected[1])

    def test_compute(self):
        """
        Tests compute aggregate wells for all fields.
        """
        ukAggregator = UkAggregator()
        ukAggregator.compute()
        fieldProductions = FieldProduction.objects.filter(name="Field3").all()
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
        self.assertEqual(fieldProductions[0].name, "Field3")
        self.assertEqual(fieldProductions[0].date, date(1995, 1, 1))
        self.assertEqual(fieldProductions[0].production_gas, 11)
        self.assertEqual(fieldProductions[0].production_oil, 22)
        self.assertEqual(fieldProductions[0].production_water, 33)
        self.assertEqual(fieldProductions[1].name, "Field3")
        self.assertEqual(fieldProductions[1].date, date(1996, 1, 1))
        self.assertEqual(fieldProductions[1].production_gas, 104)
        self.assertEqual(fieldProductions[1].production_oil, 205)
        self.assertEqual(fieldProductions[1].production_water, 306)
