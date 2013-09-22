"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.utils import override_settings
from datetime import date
from BeautifulSoup import BeautifulSoup

from oil_and_gas.models import FieldProduction
from us_loader.models import UsRequest, UsManager
from us_loader.tasks import updateBsee

class BseeRequestTest(TestCase):
    def test_next_month(self):
        """
        Tests that month increment is working.
        """
        bseeRequest = UsRequest()
        self.assertEqual(bseeRequest.year_month, date(year=1947, month=1, day=1))
        bseeRequest.nextMonth()
        self.assertEqual(bseeRequest.year_month, date(year=1947, month=2, day=1))

    def test_get_production(self):
        """
        Tests that production is correct.
        """
        soup = BeautifulSoup("<tr><td>G03229</td><td>5</td><td>2013</td><td>304</td>" +
                             "<td>0</td><td>0</td><td>516</td><td>13,129</td><td>1</td><td>18</td></tr>")
        bseeRequest = UsRequest()
        production = bseeRequest.getProduction(soup)
        expectedProduction = FieldProduction(
            name="G03229",
            country="US",
            date=date(year=2013, month=5, day=1),
            production_oil=304,
            production_gas=516,
            depth=18,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.depth, expectedProduction.depth)

    def test_get_soup(self):
        """
        Tests that production is correct.
        """
        bseeRequest = UsRequest()
        bseeRequest.year_month = date(year=2013, month=1, day=1)
        soup = bseeRequest.getSoup(page=1)
        table = soup.find('table', border=5, width=600)
        trs = table.findAll('tr')
        self.assertEqual(len(trs), 1002)

    def test_get_productions(self):
        """
        Tests that production is correct.
        """
        bseeRequest = UsRequest()
        bseeRequest.year_month = date(year=2013, month=1, day=1)
        productions = bseeRequest.getProductions()
        self.assertEqual(len(productions), 1302)
        production = productions[0]
        expectedProduction = FieldProduction(
            name="G03205",
            country="US",
            date=date(year=2013, month=1, day=1),
            production_oil=17271,
            production_gas=9446,
            depth=495,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.depth, expectedProduction.depth)
        production = productions[-1]
        expectedProduction = FieldProduction(
            name="G15212",
            country="US",
            date=date(year=2013, month=1, day=1),
            production_oil=4773+34,
            production_gas=3626+9121,
            depth=140,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.depth, expectedProduction.depth)


class ProductionTest(TestCase):
    def test_production_save(self):
        """
        Tests save.
        """
        production = FieldProduction(
            name="G15161",
            country="US",
            date=date(year=2013, month=1, day=1),
            production_oil=179,
            production_gas=4407,
            depth=171,
        )
        production.save()


class BseeManagerTest(TestCase):
    def test_update(self):
        """
        Tests update.
        """
        bseeManager = UsManager()
        bseeManager.update_to = date(year=1948, month=1, day=1)
        self.assertEqual(bseeManager.getOldestDate(), date(year=1947, month=11, day=1))
        bseeManager.update()
        count = FieldProduction.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(bseeManager.getOldestDate(), date(year=1947, month=12, day=1))

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def test_async_update(self):
        result = updateBsee.delay(date(year=1948, month=1, day=1))
        self.assertEquals(result.get(), 2)
        self.assertTrue(result.successful())