from itertools import groupby
from datetime import datetime, timedelta, date
import numpy as np

from constants import *
from OilField import *
from Wellbore import *

class CsvToOilField(object):
    """description of class"""

    def __init__(self, indexedCsv):
        self.OilFields = []
        for name, production in groupby(indexedCsv, lambda x: x[0]):
            self.addField(name, production)
        self.IndexedFields = {}
        self.createFieldIndex()
    
    def createFieldIndex(self):
        self.IndexedFields = {}
        for field in self.OilFields:
            self.IndexedFields[field.Name] = field

    def addField(self, name, production):
        oilField = OilField()
        oilField.Name = name
        for productionData in production:
            productionSpan = ProductionSpan()
            year = int(productionData[1])
            month = int(productionData[2])
            productionSpan.Start = datetime(year, month, 1)
            produced = float(productionData[3])
            if np.isnan(produced):
                produced = 0
            productionSpan.Total = produced * 1E6 / M3_TO_BARRELS
            oilField.ProductionSpans.append(productionSpan)
        Utilities.joinProductionSpans(oilField.ProductionSpans)
        oilField.smoothen()
        self.OilFields.append(oilField)
    
    def addWellInformations(self, indexedCsv):
        for name, wellboreData in groupby(indexedCsv, lambda x: x[0]):
            self.addWellInformation(name, wellboreData)

    def addWellInformation(self, name, wellboreDatas):
        if name in self.IndexedFields:
            field = self.IndexedFields[name]
            for wellboreData in wellboreDatas:
                wellbore = Wellbore()
                wellbore.Purpose = wellboreData[1]
                completion = str(wellboreData[2])
                if completion != "nan":
                    wellbore.Completion = datetime.strptime(completion, "%d.%m.%Y")
                field.Wellbores.append(wellbore)

    def numberFields(self):
        return len(self.OilFields)
