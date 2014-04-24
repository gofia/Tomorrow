from pandas import DataFrame
from pandas import Timestamp
from pandas import MultiIndex
from pandas import concat
from pandas import read_csv
from pandas import read_html

from pickle import dump
from pickle import load

from numpy import nan

from itertools import product

import os

import re

from _constants import M3_TO_BARRELS

from _config import DPATH

def get_production(country, until='2013-02-01'):
    """Return a DataFrame where the index are the dates and columns are the
    monthly production of each of the country's oil fields. File downloadable on
    http://factpages.npd.no/factpages/ under Field -> Production.

    Args:
        country -> str.
            The string representing the name of the coutry. Ex: 'NO' for Norway,
            'UK' for the United Kingdom.
        until -> str.
            The string representing the date until which the production should
            be returned.
    Return:
        production -> DataFrame.
            The DataFrame containing the timeseries of monthly oil production.
    """ 

    file_path = os.path.join(DPATH, '%s_monthly_oil_production.pkl' % country)

    if os.path.exists(file_path):
        f = open(file_path)
        df = load(f)
        return df[:until].dropna(how='all', axis=1).dropna(how='all', axis=0)
    else:
        print 'Getting the data...'
        f = open(file_path, 'w')

    os.chdir(DPATH)

    if country == 'NO':
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
        #source: http://pandas.pydata.org/pandas-docs/dev/io.html#reading-
                       #dataframe-objects-with-multiindex
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
        #We now have a MultiIndexed DataFrame with only two hierarchies: 
        #field_name and date. It might have been an overkill because in the end 
        #I want a DataFrame with index=dates columns=field_name and values and 
        #monthly production.
        field_names = level0
        dfs = []
        for field_name in field_names:
            _df = fields_df.ix[field_name]
            _df = _df[_df!=0].dropna()
            _df.columns = [field_name,]
            dfs.append(_df)
        production = concat(dfs, axis=1).dropna(axis=1, how='all')
        #converting millions of cubic meters to barrels.
        production = 1e6 * M3_TO_BARRELS * production
        production.name = 'NO monthly oil production'
    
        #Correcting for problematic oil fields
        production['BALDER'][:'1999-10-01'] = nan
        production['GRANE'][:'2003-10-01'] = nan
    
    
    if country == 'UK':
        field_ids = range(278)
        urls = ['https://www.og.decc.gov.uk/pprs/full_production/oil+production'
                +'+sorted+by+field/%s.htm' % field_id for field_id in field_ids]
        dfs = []
        for url in urls:
            field = str(read_html(url, match='^[A-Z][A-Z][A-Z]')[0].values.\
                        flatten()[0])
            _df = read_html(url, match='Yearly Total', infer_types=False, 
                            index_col=0, header=0)[0]
            #We now format production from      Jan Feb    to         field name
            #                              2009 p0  p1        01-2009 p0
            #                              2010 p12 p13       01-2010 p1
            #                              ...                ...
            months = [str(month) for month in _df.columns[:-1]]
            years = [str(year) for year in _df.index]
            _dates = list(product(months, ['-'], years))
            dates = sorted([Timestamp('01-'+''.join(date)) for date in _dates])
            df = DataFrame(index=dates, columns=[field])
            for year in years:
                for month in months:
                    monthly_production = _df[month].ix[year]
                    if monthly_production != '' and monthly_production != '0':
                        df.ix[Timestamp('01-'+str(month)+str(year))] =\
                              float(''.join(monthly_production.split(',')))
            dfs.append(df)
        production = concat(dfs, axis=1).astype('float32').dropna(how='all',
                         axis=0)
        production.name = 'UK monthly oil production'
 
    os.chdir('..')
    
    dump(production, f)
    return production[:until].dropna(how='all', axis=1).dropna(how='all', 
                                  axis=0)


def get_classification(country, until):
    """Return the DataFrame containing the classification of the different oil
    fields.

    Args: 
        country -> str.
            The string representing the name of the coutry. Ex: 'NO' for Norway,
            'UK' for the United Kingdom.
        until -> str.
            The string representing the date until which the production 
            DataFrame should be taken into account to make the classification.
    Return:
        classification -> DataFrame.
            The DataFrame containing the classif of monthly oil production.
    """    
    fpath = os.path.join(DPATH, '%s_classification.pkl' % country)
    f = open(fpath)
    classification = load(f)
    return classification.ix[until]



