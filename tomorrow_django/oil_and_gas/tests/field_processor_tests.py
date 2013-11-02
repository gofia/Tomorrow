from oil_and_gas.fitting import get_stretched_exponential

__author__ = 'lucas.fievet'

from django.test import TestCase
from datetime import datetime
from numpy import exp

from oil_and_gas.models import FieldProduction, Field, FieldProcessor


class FieldProcessorTest(TestCase):
    def setUp(self):
        func = get_stretched_exponential(100, -1.5, 2)
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 1, 1),
            production_oil=func(0)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 2, 1),
            production_oil=func(-1)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 3, 1),
            production_oil=func(-2)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 4, 1),
            production_oil=func(-3)
        )

    def test_process_field(self):
        fieldProcessor = FieldProcessor()
        fieldProcessor.compute()
        fields = Field.objects.all()
        self.assertEqual(len(fields), 1, "Wrong number of fields")
        field = fields[0]
        self.assertEqual(field.name, "A", "Wrong name")
        self.assertEqual(field.country, "B", "Wrong country")
        self.assertEqual(len(field.fits.all()), 2, "Wrong number of fits")
        self.assertAlmostEqual(field.A, 100, delta=1, msg="Wrong A")
        self.assertAlmostEqual(field.tau, -1.5, delta=0.05, msg="Wrong tau")
        self.assertAlmostEqual(field.beta, 2.0, delta=0.05, msg="Wrong beta")