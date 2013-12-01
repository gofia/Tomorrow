import copy
from django.test import TestCase
from numpy import array
from numpy.testing import assert_array_equal

from ..discovery import (SizeBins, optimize, optimize_sizes_brute, likelihood,
                         initial_x, get_constraints, size_constraints)
from oil_and_gas.utils import traverse, list_get


class DiscoveryTest(TestCase):
    sizes = [5, 1, 2, 1, 4]

    def test_size_bins_processing(self):
        # Initialising
        size_bins = SizeBins(min(self.sizes), max(self.sizes), 2)
        self.assertEqual(len(size_bins.bins), 2, "Number bins is incorrect")
        size_bin1 = size_bins.bins[0]
        size_bin2 = size_bins.bins[1]
        self.assertEqual(size_bin1.min, 1, "Min 1 is incorrect")
        self.assertEqual(size_bin1.max, 3, "Max 1 is incorrect")
        self.assertEqual(size_bin2.min, 3, "Min 2 is incorrect")
        self.assertEqual(size_bin2.max, 5, "Max 2 is incorrect")

        # Processing
        size_bins.process(self.sizes)
        assert_array_equal(size_bins.sequence, [1, 0, 0, 0, 1], "Size sequence is incorrect")

        self.assertEqual(size_bin1.count, 3, "Count 1 is incorrect")
        assert_array_equal(size_bin1.m, [0, 0, 1, 2, 3, 3], "m 1 is incorrect")

        self.assertEqual(size_bin2.count, 2, "Count 2 is incorrect")
        assert_array_equal(size_bin2.m, [0, 1, 1, 1, 1, 2], "m 2 is incorrect")

        self.assertEqual(size_bins.m(3, 1), 1, "Count 2 is incorrect")
        assert_array_equal(size_bins.m_s(3), [2, 1], "m 2 is incorrect")

    def test_likelihood_function(self):
        size_bins = SizeBins(min(self.sizes), max(self.sizes), 2)
        size_bins.process(self.sizes)
        L = likelihood(size_bins)
        expected = -1.0
        expected *= 3 * 1.0 / (3 + 4 * 0.5)
        expected *= 4 * 0.5 / (2 + 4 * 0.5)
        expected *= 3 * 0.5 / (2 + 3 * 0.5)
        expected *= 2 * 0.5 / (2 + 2 * 0.5)
        expected *= 2 * 1.0 / (2 + 1 * 0.5)
        self.assertEqual(L([4, 3, 0.5]), expected, "Likelihood is incorrect")

    def test_optimize_sizes(self):
        sizes = [5, 1, 4, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 4]
        print len(sizes)
        result = optimize(sizes)
        grid_points = []
        for i in traverse(result[3]):
            grid_points.append(copy.deepcopy(i))
        grid_points.sort(key=lambda item: item[0])
        for i in grid_points:
            print "{0}".format(i)
            print "{0}".format(list_get(result[2], i[1]))
        #print result[0]
        #print result[1]
        #print result[2]
        #print result[3]
