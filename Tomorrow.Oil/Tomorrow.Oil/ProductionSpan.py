from datetime import datetime, timedelta

class ProductionSpan(object):
    """Represents a production span"""

    def __init__(self):
        self.Start = datetime.today()
        self.End = datetime.today()
        self.Total = 0
    
    @classmethod
    def instance(cls, start, end, total):
        productionSpan = cls()
        productionSpan.Start = start
        productionSpan.End = end
        productionSpan.Total = total
        return productionSpan
    
    def span(self):
        return self.End - self.Start

    def flux(self):
        flux = self.Total / self.span().days
        return flux

    def __add__(self, other):
        self.Start = min(self.Start, other.Start)
        self.End = max(self.End, other.End)
        self.Total += other.Total
        return self

    def __repr__(self):
        return self.Start.__str__() + " -> " + self.End.__str__() + ": " + self.Total.__str__()