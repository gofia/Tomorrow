from django.test import TestCase
from django.test.utils import override_settings
from datetime import date
from BeautifulSoup import BeautifulSoup

from oil_and_gas.models import FieldProduction
from no_loader.models import NoManager

class NoManagerTest(TestCase):
    def test_get_csv(self):
        """
        Tests that update is correct.
        """
        noManager = NoManager()
        noManager.update()
        #expectedProduction = WellProduction(
        #    country="UK",
        #    date=date(year=1995, month=1, day=1),
        #    production_oil=46742,
        #    production_gas=2184,
        #    production_water=1035,
        #)
        #self.assertEqual(production.country, expectedProduction.country)
        #self.assertEqual(production.date, expectedProduction.date)
        #self.assertEqual(production.production_oil, expectedProduction.production_oil)
        #self.assertEqual(production.production_gas, expectedProduction.production_gas)
        #self.assertEqual(production.production_water, expectedProduction.production_water)