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
        noManager.update(5)
        productions = FieldProduction.objects.filter(country="NO").all()
        self.assertEqual(len(productions), 4)
        self.assertEqual(productions[0].name, "33/9-6 DELTA")
        self.assertEqual(productions[0].date.year, 2009)
        self.assertEqual(productions[0].date.month, 7)
        self.assertEqual(productions[0].production_oil, 2096)