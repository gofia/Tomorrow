from datetime import datetime

class Wellbore(object):
    """description of class"""

    def __init__(self):
        self.Purpose = "UNKOWN"
        self.Completion = datetime.now()

    def __repr__(self):
        return self.Purpose.__str__() + " -> " + self.Completion.__str__()