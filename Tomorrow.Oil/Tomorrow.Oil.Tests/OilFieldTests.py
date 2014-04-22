import sys
from datetime import datetime, timedelta
import unittest

sys.path.append("../Tomorrow.Oil")

from OilField import OilField
from ProductionSpan import ProductionSpan

class Test_OilFieldTests(unittest.TestCase):
    
    def testName(self):
        self.OilField = OilField()
        self.OilField.Name = "Frigg"
        self.assertEqual("Frigg", self.OilField.Name)

    def testTotalProduction(self):
        oilField = OilField()
        t0 = datetime.now() - timedelta(days=2)
        t1 = datetime.now() - timedelta(days=1)
        t2 = datetime.now()
        oilField.ProductionSpans.append(ProductionSpan.instance(t0, t1, 10))
        oilField.ProductionSpans.append(ProductionSpan.instance(t1, t2, 6))
        self.assertEqual(oilField.totalProduction(), 16)
        self.assertEqual(oilField.discovery(), t0)
        
    def testToString(self):
        oilField = OilField()
        oilField.Name = "Frigg"
        t0 = datetime.now() - timedelta(days=2)
        t1 = datetime.now() - timedelta(days=1)
        t2 = datetime.now()
        oilField.ProductionSpans.append(ProductionSpan.instance(t0, t1, 10))
        oilField.ProductionSpans.append(ProductionSpan.instance(t1, t2, 6))
        print oilField

if __name__ == '__main__':
    unittest.main()
