"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import date
from BeautifulSoup import BeautifulSoup

from bsee_loader.models import Production, BseeRequest, BseeManager

class BseeRequestTest(TestCase):
    def test_next_month(self):
        """
        Tests that month increment is working.
        """
        bseeRequest = BseeRequest()
        self.assertEqual(bseeRequest.year_month, date(year=1947, month=1, day=1))
        bseeRequest.nextMonth()
        self.assertEqual(bseeRequest.year_month, date(year=1947, month=2, day=1))

    def test_get_production(self):
        """
        Tests that production is correct.
        """
        soup = BeautifulSoup("<tr><td>G03229</td><td>5</td><td>2013</td><td>304</td>" +
                             "<td>0</td><td>0</td><td>516</td><td>13,129</td><td>1</td><td>18</td></tr>")
        bseeRequest = BseeRequest()
        production = bseeRequest.getProduction(soup)
        expectedProduction = Production(
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
        bseeRequest = BseeRequest()
        bseeRequest.year_month = date(year=2013, month=1, day=1)
        soup = bseeRequest.getSoup(page=1)
        table = soup.find('table', border=5, width=600)
        trs = table.findAll('tr')
        self.assertEqual(len(trs), 1002)

    def test_get_productions(self):
        """
        Tests that production is correct.
        """
        bseeRequest = BseeRequest()
        bseeRequest.year_month = date(year=2013, month=1, day=1)
        productions = bseeRequest.getProductions()
        self.assertEqual(len(productions), 1300)
        production = productions[0]
        expectedProduction = Production(
            name="G03197",
            country="US",
            date=date(year=2013, month=1, day=1),
            production_oil=8741,
            production_gas=72970,
            depth=44,
        )
        self.assertEqual(production.name, expectedProduction.name)
        self.assertEqual(production.country, expectedProduction.country)
        self.assertEqual(production.date, expectedProduction.date)
        self.assertEqual(production.production_oil, expectedProduction.production_oil)
        self.assertEqual(production.production_gas, expectedProduction.production_gas)
        self.assertEqual(production.depth, expectedProduction.depth)
        production = productions[-1]
        expectedProduction = Production(
            name="G15161",
            country="US",
            date=date(year=2013, month=1, day=1),
            production_oil=179,
            production_gas=4407,
            depth=171,
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
        production = Production(
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
        bseeManager = BseeManager()
        bseeManager.update_to = date(year=1948, month=1, day=1)
        self.assertEqual(bseeManager.getOldestDate(), date(year=1947, month=11, day=1))
        bseeManager.update()
        count = Production.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(bseeManager.getOldestDate(), date(year=1947, month=12, day=1))