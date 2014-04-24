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
from datetime import date

from ..models import Field
from ..processing import CountryProcessor
from ..fitting import get_stretched_exponential


class CountryProcessorTest(TestCase):
    field = None

    def setUp(self):
        self.field = Field.objects.create(
            name="A",
            country="B",
            date_begin=date(year=2001, month=1, day=1),
            x_min=12,
            A=100.0,
            tau=-1.5,
            beta=2.0,
            error_avg=0.01,
            error_std=0.01,
        )

    def tearDown(self):
        self.field.delete()

    def test_init_forecasts(self):
        processor = CountryProcessor()
        forecasts = processor.init_forecasts(date(year=2000, month=1, day=1), 24)
        self.assertEqual(len(forecasts), 24, "Wrong length")
        self.assertEqual(forecasts[0]['date'], date(year=2000, month=1, day=1), "Wrong start date")
        self.assertEqual(forecasts[-1]['date'], date(year=2001, month=12, day=1), "Wrong end date")

    def test_forecast_field(self):
        field = self.field
        processor = CountryProcessor()
        forecasts = processor.init_forecasts(date(year=2000, month=1, day=1), 24)
        processor.forecast(field, forecasts)
        self.assertEqual(len(forecasts), 24, "Wrong length")
        self.assertEqual(forecasts[0]['average'], 0, "Wrong average")
        self.assertEqual(forecasts[0]['sigma'], 0, "Wrong sigma")
        self.assertEqual(forecasts[11]['average'], 0, "Wrong average")
        self.assertEqual(forecasts[11]['sigma'], 0, "Wrong sigma")

        func = get_stretched_exponential(field.A, field.tau, field.beta)

        y_23 = func(field.x_min + 11) * (1 - field.error_avg)
        f_23_avg = forecasts[23]['average']
        self.assertEqual(f_23_avg, y_23, "Wrong average: {0} vs {1}.".format(f_23_avg, y_23))

        sigma_23 = (y_23 * field.error_std)**2
        f_23_sigma = forecasts[23]['sigma']
        self.assertEqual(
            f_23_sigma,
            sigma_23,
            "Wrong sigma: {0} vs {1}.".format(f_23_sigma, sigma_23)
        )
