from django.test import TestCase
from numpy import array
from numpy.testing import assert_array_equal

from ..fitting import prepare_xy, chop_xy, x_min_2_x_min


class FittingTest(TestCase):
    def test_prepare_xy(self):
        x = [1, 2, 3, 4]
        y = [-1, -2, -3, -4]
        result = prepare_xy(x, y)
        expected = (array([1, 2, 3, 4]), [-1, -2, -3, -4])
        assert_array_equal(result[0], expected[0], "Prepared result is incorrect")
        self.assertEqual(result[1], expected[1], "Prepared result is incorrect")

    def test_chop_xy(self):
        x = array([1, 2, 3, 4])
        y = array([-1, -2, -3, -4])
        result_x, result_y = chop_xy(x, y, 2, 4)
        expected_x = array([2, 3])
        expected_y = array([-2, -3])
        assert_array_equal(result_x, expected_x, "Chopped result x is incorrect")
        assert_array_equal(result_y, expected_y, "Chopped result y is incorrect")

    def test_x_min_2_x_min(self):
        x_ = [1, 2, 3, 4]
        y_ = [0, 5, 11, 8]
        _x, _y = prepare_xy(x_, y_)
        result = x_min_2_x_min('max', x_, y_, _x, _y)
        expected = 3
        self.assertEqual(result, expected, "Result is incorrect")
