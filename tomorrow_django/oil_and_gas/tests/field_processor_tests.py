__author__ = 'lucas.fievet'

from django.test import TestCase
from datetime import datetime
from numpy import exp

from oil_and_gas.models import FieldProduction, Field, FieldProcessor


class FieldProcessorTest(TestCase):
    def setUp(self):
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 1, 1),
            production_oil=100*exp(0)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 2, 1),
            production_oil=100*exp(-1)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 3, 1),
            production_oil=100*exp(-2)
        )
        FieldProduction.objects.create(
            name="A",
            country="B",
            date=datetime(2000, 4, 1),
            production_oil=100*exp(-3)
        )

    def test_process_field(self):
        fieldProcessor = FieldProcessor()
        fieldProcessor.compute()
        fields = Field.objects.all()
        self.assertEqual(len(fields), 1, "Wrong number of fields")
        field = fields[0]
        self.assertEqual(field.name, "A", "Wrong name")
        self.assertEqual(field.country, "B", "Wrong country")
        print field.A
        print field.tau
        print field.beta
        self.assertAlmostEqual(field.A, 100, delta=1, msg="Wrong A")
        self.assertAlmostEqual(field.tau, -1.0, delta=0.05, msg="Wrong tau")
        self.assertAlmostEqual(field.beta, 1.0, delta=0.05, msg="Wrong beta")