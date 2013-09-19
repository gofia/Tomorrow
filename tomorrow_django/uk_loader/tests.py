"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.utils import override_settings
from datetime import date
from BeautifulSoup import BeautifulSoup

from oil_and_gas.models import WellProduction
from uk_loader.models import UkRequest, UkManager
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
