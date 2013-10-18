from pandas import Timestamp

MIN_PROD = 1.58

M3_TO_BARRELS = 1. / 6.2898

START = {'NO': Timestamp('1971-06-01'), 'UK': Timestamp('1975-06-01')}

BOUNDS = {'NO': {'2013-02-01': [1e6, 1e7],
               '2003-02-01': [1e7],},
        'UK': {'2013-02-01': [1e6, 1e7],
               '1998-02-01': [1e6, 1e7],
               '1993-02-01': [1e6, 1e7],},
       }
MAX_DATE = Timestamp('2260-01-01')
