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

from ..utils import (traverse)


class UtilsTest(TestCase):
    def test_traverse(self):
        nested_list = [1, [2, 2.3, 2.6, [2.7, 2.8, 2.9]], 3]
        index = 0
        expected = [
            (1, [0]),
            (2, [1, 0]),
            (2.3, [1, 1]),
            (2.6, [1, 2]),
            (2.7, [1, 3, 0]),
            (2.8, [1, 3, 1]),
            (2.9, [1, 3, 2]),
            (3, [2]),
        ]
        for i in traverse(nested_list):
            self.assertEqual(i, expected[index])
            index += 1
