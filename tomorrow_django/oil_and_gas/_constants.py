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

OIL_PRICE_SINCE_2000 = [
    25.21,
    27.15,
    27.49,
    23.45,
    27.23,
    29.62,
    28.16,
    29.41,
    32.08,
    31.4,
    32.33,
    25.28,
    25.95,
    27.24,
    25.02,
    25.66,
    27.55,
    26.97,
    24.8,
    25.81,
    25.03,
    20.73,
    18.69,
    18.52,
    19.15,
    19.98,
    23.64,
    25.43,
    25.69,
    24.49,
    25.75,
    26.78,
    28.28,
    27.53,
    24.79,
    27.89,
    30.77,
    32.88,
    30.36,
    25.49,
    26.06,
    27.91,
    28.59,
    29.68,
    26.88,
    29.01,
    29.12,
    29.95,
    31.4,
    31.32,
    33.67,
    33.71,
    37.63,
    35.54,
    37.93,
    42.08,
    41.65,
    46.87,
    42.23,
    39.09,
    42.89,
    44.56,
    50.93,
    50.64,
    47.81,
    53.89,
    56.37,
    61.87,
    61.65,
    58.19,
    54.98,
    56.47,
    62.36,
    59.71,
    60.93,
    68,
    68.61,
    68.29,
    72.51,
    71.81,
    61.97,
    57.95,
    58.13,
    61,
    53.4,
    57.58,
    60.6,
    65.1,
    65.1,
    68.19,
    73.67,
    70.13,
    76.91,
    82.15,
    91.27,
    89.43,
    90.82,
    93.75,
    101.84,
    109.05,
    122.77,
    131.52,
    132.55,
    114.57,
    99.29,
    72.69,
    54.04,
    41.53,
    43.91,
    41.76,
    46.95,
    50.28,
    58.1,
    69.13,
    64.65,
    71.63,
    68.38,
    74.08,
    77.56,
    74.88,
    77.12,
    74.72,
    79.3,
    84.14,
    75.54,
    74.73,
    74.52,
    75.88,
    76.11,
    81.72,
    84.53,
    90.07,
    92.66,
    97.73,
    108.65,
    116.32,
    108.18,
    105.85,
    107.88,
    100.45,
    100.83,
    99.92,
    105.36,
    104.26,
    106.89,
    112.7,
    117.79,
    113.75,
    104.16,
    90.73,
    96.75,
    105.28,
    106.32,
    103.39,
    101.17,
    101.17,
    105.04,
    107.66,
    102.61,
    98.85,
    99.35,
    99.74,
    105.21,
    108.06,
    108.78,
    105.46,
    102.58,
    105.49,
    102.25,
    104.82,
    104.04,
    104.94,
    105.73,
    108.37,
]
