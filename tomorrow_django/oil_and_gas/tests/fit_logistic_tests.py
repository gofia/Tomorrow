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
from numpy import array

from ..fit_logistic import (fit_logistic_r_p, get_logistic, get_d_logistic,
                            fit_d_logistic_r_k_p)


class FittingTest(TestCase):
    def test_fit_logistic_r_p(self):
        func = get_logistic(2.0, 3.0, 5.0)
        x = array([0, 1, 2, 3])
        y = [func(0.0), func(1.0), func(2.0), func(3.0)]
        r, p, residual = fit_logistic_r_p(3.0, x, y)
        self.assertAlmostEqual(r, 2.0, delta=0.01, msg="r is incorrect")
        self.assertAlmostEqual(p, 5.0, delta=0.01, msg="p is incorrect")

    def test_fit_d_logistic(self):
        func = get_d_logistic(2.0, 3.0, 5.0)
        x = array([0, 1, 2, 3])
        y = [func(0.0), func(1.0), func(2.0), func(3.0)]
        r, k, p, residual = fit_d_logistic_r_k_p(x, y)
        self.assertAlmostEqual(r, 2.0, delta=0.01, msg="r={0} is incorrect".format(r))
        self.assertAlmostEqual(k, 3.0, delta=0.01, msg="k={0} is incorrect".format(k))
        self.assertAlmostEqual(p, 5.0, delta=0.01, msg="p={0} is incorrect".format(p))
