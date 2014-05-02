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

from ..fit_logistic import fit_logistic_k_r, get_logistic


class FittingTest(TestCase):
    def test_stretched_exponential(self):
        func = get_logistic(2.0, 3.0, 5.0)
        x = array([0, 1, 2, 3])
        y = [func(0.0), func(1.0), func(2.0), func(3.0)]
        k, r, residual = fit_logistic_k_r(5.0, x, y)
        self.assertAlmostEqual(k, 3.0, delta=0.01, msg="k is incorrect")
        self.assertAlmostEqual(r, 2.0, delta=0.01, msg="r is incorrect")
