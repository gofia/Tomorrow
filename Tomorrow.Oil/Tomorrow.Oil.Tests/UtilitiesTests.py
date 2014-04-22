import sys
import unittest

sys.path.append("../Tomorrow.Oil")

from Utilities import Utilities

class Test_UtilitiesTests(unittest.TestCase):
    def testTotalChange(self):
        array = [{"a": 1}, {"a": 2}, {"a": 0.5}, {"a": 3}]
        change = Utilities.totalChange(array, lambda e: e["a"])
        self.assertEqual(change, 5)

    def testGroup(self):
        array = [1, 2, 3, 4]
        change = Utilities.group(array, 2)
        self.assertEqual(change, [[1, 2], [3, 4]])

    def testGroupAndMerge(self):
        array = [1, 2, 3, 4]
        change = Utilities.groupAndMerge(array, 2)
        self.assertEqual(change, [3, 7])

    def testMovingAverage(self):
        array = [1, 2, 3, 4]
        average = Utilities.movingAverage(array, 1)
        self.assertEqual(average, [1.5, 2, 3, 3.5])

if __name__ == '__main__':
    unittest.main()
