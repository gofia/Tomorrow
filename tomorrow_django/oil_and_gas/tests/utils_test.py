from django.test import TestCase
from numpy import array, exp
from numpy.testing import assert_array_equal

from ..utils import (traverse)


class UtilsTest(TestCase):
    def test_traverse(self):
        nested_list = [1, [2, 2.3, 2.6, [2.7, 2.8, 2.9]], 3]
        for i in traverse(nested_list):
            print "{0}".format(i)
