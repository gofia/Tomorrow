from django.test import TestCase
from datetime import date
from numpy import array, exp
from numpy.testing import assert_array_equal

from ..fit_logistic import (get_logistic, fit_logistic, get_d_logistic, fit_d_logistic)


class FittingTest(TestCase):
    def test_stretched_exponential(self):
        func = get_d_logistic(2.0, 10.0, 1.0)
        _dates = [
            date(year=2010, month=1, day=1),
            date(year=2011, month=1, day=1),
            date(year=2012, month=1, day=1),
            date(year=2013, month=1, day=1)
        ]
        _y = [func(0.0), func(1.0), func(2.0), func(3.0)]
        r, k, p = fit_d_logistic(_dates, _y, _dates[0], (10.0, 1.0))
        print r
        print k
        print p
        print _y
        print get_d_logistic(r, k, p)([0.0, 1.0, 2.0, 3.0])
        self.assertAlmostEqual(r, 2.0, delta=0.01, msg="r is incorrect")
        self.assertAlmostEqual(k, 10.0, delta=0.01, msg="k is incorrect")
        self.assertAlmostEqual(p, 1.0, delta=0.01, msg="p is incorrect")
