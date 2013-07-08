from copy import deepcopy

from ProductionSpan import *
from Utilities import *

class OilField(object):
    """Represents an oil field"""

    def __init__(self):
        self.Name = ""
        self.ProductionSpans = []
        self.Wellbores = []

    def totalProduction(self):
        total = 0
        for productionSpan in self.ProductionSpans:
            total += productionSpan.Total
        return total

    def productionList(self):
        start = self.discovery()
        months = [(p.Start.year - start.year) * 12 + (p.Start.month - start.month) 
                  for p in self.ProductionSpans]
        fluxes = [p.flux() for p in self.ProductionSpans]
        r = int(len(self.ProductionSpans) * 0.05)
        fluxes = Utilities.movingAverage(fluxes, r)
        return { "months": months, "fluxes": fluxes }
    
    def smoothenProductionList(self):
        start = self.discovery()
        months = [(p.Start.year - start.year) * 12 + (p.Start.month - start.month) 
                  for p in self.SmoothenProductionSpans]
        fluxes = [p.flux() for p in self.SmoothenProductionSpans]
        return { "months": months, "fluxes": fluxes }

    def discovery(self):
        self.ProductionSpans.sort(key=lambda x: x.Start)
        return self.ProductionSpans[0].Start

    def smoothen(self):

        fluxLambda = lambda ps: ps.flux()

        smoothestAverageChange = Utilities.averageChange(self.ProductionSpans, fluxLambda)
        smoothestGroupSize = 1

        for groupSize in range(2,12):
            p = deepcopy(self.ProductionSpans)
            p = Utilities.groupAndMerge(p, groupSize)
            newAverageChange = Utilities.averageChange(p, fluxLambda)
            if newAverageChange < smoothestAverageChange:
                smoothestAverageChange = newAverageChange
                smoothestGroupSize = groupSize

        p = deepcopy(self.ProductionSpans)
        self.SmoothenProductionSpans = Utilities.groupAndMerge(p, smoothestGroupSize)
    
    def productionWellDates(self):
        start = self.discovery()
        months = [(w.Completion.year - start.year) * 12 + (w.Completion.month - start.month) 
                  for w in self.Wellbores]
        return months

    def __repr__(self):
        str = self.Name + "\n"
        for productionSpan in self.ProductionSpans:
            str += productionSpan.__str__() + "\n"
        return str






