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

from oil_and_gas.models import FieldProduction
from .models import NoManager


class NoManagerTest(TestCase):
    def test_get_csv(self):
        """
        Tests that update is correct.
        """
        no_manager = NoManager()
        no_manager.update(5)
        productions = FieldProduction.objects.filter(country="NO").all()
        self.assertEqual(len(productions), 4)
        self.assertEqual(productions[0].name, "33/9-6 DELTA")
        self.assertEqual(productions[0].date.year, 2009)
        self.assertEqual(productions[0].date.month, 7)
        self.assertEqual(productions[0].production_oil, 2096)