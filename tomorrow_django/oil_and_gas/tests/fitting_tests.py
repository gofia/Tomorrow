"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from ..fitting import chop_xy


class FittingTest(TestCase):
    def test_chop_xy(self):
        x = [1, 2, 3, 4]
        y = [1, 2, 3, 4]
        result = chop_xy(x, y, 2, 4)
        expected = ([2, 3, 4], [2, 3, 4])
        self.assertEqual(result, expected, "Chopped result is incorrect")
