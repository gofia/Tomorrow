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
from django.test.utils import override_settings
from datetime import date
from BeautifulSoup import BeautifulSoup

from oil_and_gas.models import FieldProduction
from .models import UkRequest, UkManager
from .tasks import update_uk


class UkRequestTest(TestCase):
    def test_get_production(self):
        """
        Tests that production is correct.
        """
        soup = BeautifulSoup('<tr>'
                             '<td  class="s10">2009</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s11">&nbsp;</td>'
                             '<td  class="s12">10,270</td>'
                             '<td  class="s12">798</td>'
                             '<td  class="s12">0</td>'
                             '<td  class="s12">344</td>'
                             '<td  class="s12">30</td>'
                             '<td  class="s13">11,442</td>'
                             '</tr>')
        uk_request = UkRequest()
        productions = uk_request.get_production(soup, "Name")
        expected_production = FieldProduction(
            country="UK",
            name="Name",
            date=date(year=2009, month=9, day=1),
            production_oil=798,
        )
        self.assertEqual(len(productions), 12)
        production = productions[8]
        self.assertEqual(production.country, expected_production.country)
        self.assertEqual(production.date, expected_production.date)
        self.assertEqual(production.name, expected_production.name)
        self.assertEqual(production.production_oil, expected_production.production_oil)
        self.assertEqual(production.production_gas, expected_production.production_gas)
        self.assertEqual(production.production_water, expected_production.production_water)

    def test_get_soup(self):
        """
        Tests that production is correct.
        """
        uk_request = UkRequest()
        soup = uk_request.get_soup(page=0)
        table = soup.find('table', width="861", cellspacing="0")
        trs = table.findAll('tr')
        self.assertEqual(len(trs), 6)

    def test_get_production_page(self):
        """
        Tests that production is correct.
        """
        uk_request = UkRequest()
        productions = uk_request.get_production_page(0)
        self.assertEqual(len(productions), 60)
        production = productions[0]
        expected_production = FieldProduction(
            name="AFFLECK",
            country="UK",
            date=date(year=2009, month=1, day=1),
            production_oil=0,
        )
        self.assertEqual(production.name, expected_production.name)
        self.assertEqual(production.country, expected_production.country)
        self.assertEqual(production.date, expected_production.date)
        self.assertEqual(production.production_oil, expected_production.production_oil)
        self.assertEqual(production.production_gas, expected_production.production_gas)
        self.assertEqual(production.production_water, expected_production.production_water)
        production = productions[-1]
        expected_production = FieldProduction(
            name="AFFLECK",
            country="UK",
            date=date(year=2013, month=12, day=1),
            production_oil=5462,
        )
        self.assertEqual(production.name, expected_production.name)
        self.assertEqual(production.country, expected_production.country)
        self.assertEqual(production.date, expected_production.date)
        self.assertEqual(production.production_oil, expected_production.production_oil)
        self.assertEqual(production.production_gas, expected_production.production_gas)
        self.assertEqual(production.production_water, expected_production.production_water)


class UkManagerTest(TestCase):
    def test_update(self):
        """
        Tests update.
        """
        uk_manager = UkManager()
        self.assertEqual(uk_manager.get_youngest_date(0), date(year=1947, month=11, day=1))
        uk_manager.update(1)
        count = FieldProduction.objects.count()
        self.assertEqual(count, 300)
        self.assertEqual(uk_manager.get_youngest_date("AFFLECK"), date(year=2013, month=12, day=1))

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory',)
    def test_async_update(self):
        result = update_uk.delay(2)
        self.assertEquals(result.get(), 624)
        self.assertTrue(result.successful())
