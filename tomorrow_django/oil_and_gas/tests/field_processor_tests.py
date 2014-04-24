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
from datetime import datetime

from ..models import FieldProduction, Field
from ..processing import FieldProcessor
from ..fitting import get_stretched_exponential


class FieldProcessorTest(TestCase):
    production1, production2, production3, production4 = None, None, None, None

    def setUp(self):
        func = get_stretched_exponential(100, -1.5, 2)
        self.production1 = FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 1, 1),
            production_oil=func(0)
        )
        self.production2 = FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 2, 1),
            production_oil=func(-1)
        )
        self.production3 = FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 3, 1),
            production_oil=func(-2)
        )
        self.production4 = FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 4, 1),
            production_oil=func(-3)
        )

    def tearDown(self):
        self.production1.delete()
        self.production2.delete()
        self.production3.delete()
        self.production4.delete()

    def test_process_field(self):
        field_processor = FieldProcessor()
        field_processor.compute("B")
        fields = Field.objects.all()
        self.assertEqual(len(fields), 1, "Wrong number of fields")
        field = fields[0]
        self.assertEqual(field.name, "A", "Wrong name")
        self.assertEqual(field.country, "B", "Wrong country")
        n_fits = len(field.fits.all())
        self.assertEqual(n_fits, 2, "Wrong number of fits: {0}/{1}.".format(n_fits, 1))
        self.assertAlmostEqual(field.A, 100, delta=1, msg="Wrong A")
        self.assertAlmostEqual(field.tau, -1.5, delta=0.05, msg="Wrong tau")
        self.assertAlmostEqual(field.beta, 2.0, delta=0.05, msg="Wrong beta")
