import sys
import os
import unittest
from datetime import date
from pandas import *

sys.path.append("../Tomorrow.Oil")

from OilField import OilField
from ProductionSpan import ProductionSpan
from CsvToOilField import CsvToOilField

class Test_CsvToOilFieldTests(unittest.TestCase):
    def testPath(self):
        print os.getcwd()

    def testCsvToOilField(self):
        relativePath = '\Data\oil_production_by_fields.csv'
        absolutePath = os.getcwd() + relativePath
        indexedCsv = read_csv(absolutePath, index_col=[0, 1, 2, 3])[0:-1]
        csvToOilField = CsvToOilField(indexedCsv.index)

        self.assertEqual(csvToOilField.numberFields(), 89)

        firstOilField = csvToOilField.OilFields[0]
        self.assertEqual(len(firstOilField.ProductionSpans), 44)
        self.assertEqual(firstOilField.discovery().year, 2009)
        self.assertEqual(firstOilField.discovery().month, 7)
        self.assertEqual(firstOilField.discovery().day, 1)

        relativePath = '\Data\wellbore_developments.csv'
        absolutePath = os.getcwd() + relativePath
        indexedCsv = read_csv(absolutePath, index_col=[10, 5, 9])[0:-1]
        csvToOilField.addWellInformations(indexedCsv.index)

if __name__ == '__main__':
    unittest.main()
