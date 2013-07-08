import sys
from datetime import timedelta
import unittest

sys.path.append("../Tomorrow.Oil")

from ProductionSpan import ProductionSpan

class Test_ProductionSpanTests(unittest.TestCase):
    def testFlux(self):
        productionSpan = ProductionSpan()
        productionSpan.Start -= timedelta(days=2)
        productionSpan.Total = 10
        self.assertEqual(productionSpan.flux(), 5)

    def testSpan(self):
        productionSpan = ProductionSpan()
        productionSpan.Start -= timedelta(days=2)
        self.assertEqual(productionSpan.span().days, 2)

if __name__ == '__main__':
    unittest.main()
