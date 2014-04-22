import numpy as np
from datetime import timedelta

class Utilities(object):
    """description of class"""

    @classmethod
    def totalChange(cls, array, projection):
        values = [projection(e) for e in array]
        differences = np.diff(values)
        absDifferences = [abs(d) for d in differences]
        sum = np.sum(absDifferences)
        return sum
    
    @classmethod
    def averageChange(cls, array, projection):
        change = Utilities.totalChange(array, projection)
        averageChange = change / len(array)
        return averageChange

    @classmethod
    def groupAndMerge(cls, array, groupSize):
        grouped = Utilities.group(array, groupSize)
        merged = [np.sum(e) for e in grouped]
        return merged

    @classmethod
    def group(cls, array, groupSize):
        i=0
        new_array=[]
        while i<len(array):
          new_array.append(array[i:i+groupSize])
          i += groupSize
        return new_array

    @classmethod
    def joinProductionSpans(cls, productionSpans):
        for i in range(0, len(productionSpans)-1):
            productionSpans[i].End = productionSpans[i+1].Start
        productionSpans[-1].End = productionSpans[-1].Start + timedelta(days=30)

    @classmethod
    def movingAverage(cls, array, r):
        averagedArray = []
        for i in range(0, len(array)):
            lowerBound = max(0, i-r)
            upperBound = min(i+r+1, len(array))
            average = float(np.sum(array[lowerBound:upperBound])) / (upperBound - lowerBound)
            averagedArray.append(average)
        return averagedArray