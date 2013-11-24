from oil_and_gas.fitting import get_stretched_exponential

__author__ = 'lucas.fievet'

from django.test import TestCase
from datetime import date

from oil_and_gas.models import Field
from oil_and_gas.processing import CountryProcessor


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
        self.assertEqual(forecasts[23]['average'], y_23, "Wrong average")

        sigma_23 = (y_23 * field.error_std)**2
        self.assertEqual(forecasts[23]['sigma'], sigma_23, "Wrong sigma")