from pandas import DataFrame
from pandas import Timestamp
from pandas import MultiIndex
from pandas import concat
from pandas import read_csv

from numpy import nan

import os

import re

from constants import M3_TO_BARRELS
PATH = os.path.join(os.environ['HOME'], 'work', 'eth', 'peak_oil', 'data')

def get_oil_fields(data_file_path=PATH):
    """Return a DataFrame where the index are the dates and columns are the
    monthly production of each of the Norwegian oil fields. The only argument is
    the path to the .csv file downloadable on http://factpages.npd.no/factpages/
    under Field -> Production.
    """ 
    
    os.chdir(data_file_path)
    #Reading in the csv file. We get a MultiIndexed DataFrame with the 
    #hierarchies being field_name, year, month.
    df = read_csv('oil_production_by_fields.csv', index_col=[0, 1, 2])
    #We only need the oil production
    df = df['prfPrdOilNetMillSm3'].dropna()
    
    mind = df.index
    _mind = [(field, Timestamp('%d-%d-01' % (int(year), int(month)))) 
                for (field, year, month) in mind]
    #Dealing with Danish special characters...
    _mind = [(m[0].decode('utf-8'), m[1]) for m in _mind]
    _mind = [(re.sub(r'\xc5', 'A', m[0]), m[1]) for m in _mind]
    _mind = [(re.sub(r'\xd8', 'O', m[0]), m[1]) for m in _mind]
    #I cannot call MultiIndex(_mind) or MultiIndex(zip(*_mind)). I don't
    #understand why. So I go through the following construction:
    #In [1179]: index = MultiIndex(levels=[['foo', 'bar', 'baz', 'qux'],
    #   ......:                            ['one', 'two', 'three']],
    #   ......:                    labels=[[0, 0, 0, 1, 1, 2, 2, 3, 3, 3],
    #   ......:                            [0, 1, 2, 0, 1, 1, 2, 0, 1, 2]],
    #   ......:                    names=['foo', 'bar'])
    #source: http://pandas.pydata.org/pandas-docs/dev/io.html#reading-dataframe\
    #-objects-with-multiindex
    #todo: 7 lines -> 1 line
    level0, level1 = zip(*_mind)
    #Replacing the Danish special characters.
    level0, level1 = sorted(list(set(level0))), sorted(list(set(level1)))
    level0_to_label = dict(zip(level0, range(len(level0))))
    level1_to_label = dict(zip(level1, range(len(level1))))
    label0 = [level0_to_label[ind[0]] for ind in _mind]
    label1 = [level1_to_label[ind[1]] for ind in _mind]
    index = MultiIndex(levels=[level0, level1], labels=[label0, label1], 
        names=['field', 'time'])
    fields_df = DataFrame(df.values, index=index)
    #We now have a MultiIndexed DataFrame with only two hierarchies: field_name
    #and date. It might have been an overkill because in the end I want a
    #DataFrame with index=dates columns=field_name and values and monthly 
    #production.
    field_names = level0
    dfs = []
    for field_name in field_names:
        _df = fields_df.ix[field_name]
        _df = _df[_df!=0].dropna()
        _df.columns = [field_name,]
        dfs.append(_df)
    final_df = concat(dfs, axis=1).dropna(axis=1, how='all')
    #converting millions of cubic meters to barrels.
    final_df = 1e6 * M3_TO_BARRELS * final_df
    final_df.name = 'monthly oil production'

    #Correcting for problematic oil fields
    final_df['BALDER'][:'1999-10-01'] = nan
    final_df['GRANE'][:'2003-10-01'] = nan

    os.chdir('..')

    return final_df

