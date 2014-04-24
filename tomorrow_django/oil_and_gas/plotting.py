import matplotlib as mpl
import matplotlib.pyplot as plt

from _get_data import get_production, get_classification
from _analysis import get_fit_parms, classify_fields_according_to_urr
from fitting import prepare_xy

from numpy import exp, sign, array, arange

from pandas import Series, date_range

from pickle import load, dump

import os

from _constants import START

mpl.rcParams['font.size'] = 15.0
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
mpl.rc('text', usetex=True)

def irregular_vs_regular(w=8, l=10, save=False):
    uk_regular = 'WELTON'
    no_irregular = 'VALE'

    uk_prod = get_production('UK')[uk_regular].dropna()
    no_prod = get_production('NO')[no_irregular].dropna()

    fig = plt.figure(figsize=(w, l))
    ax = fig.add_subplot(211)
    uk_prod.plot(ax=ax, marker='x', ls='', color='b')
    l1 = ax.get_lines()[0]

    ax.set_ylabel('Production [barrels/day]')
    ax.set_title('Example of a regular field')
    ax.legend([l1], [uk_regular.lower().capitalize() + ' (UK)'])
   

    ax2 = fig.add_subplot(212)
    no_prod.plot(ax=ax2, marker='o', ls='', color='b')
    l2 = ax2.get_lines()[0]    

    ax2.set_xlabel('Time')
    ax2.set_ylabel('Production [barrels/day]')
    ax2.set_title('Example of an irregular field')
    ax2.legend([l2], [no_irregular.lower().capitalize() + ' (NO)'], 
               loc='upper left')

    fig.tight_layout()

    if save:
        os.chdir('article')
        fig.savefig('regular_and_irregular.pdf')
        os.chdir('..')
    else:
        plt.show()


def stretched_exponential(w=8, l=10, save=False):
    field = 'WELTON'
    prod = get_production('UK')[field].dropna()
    fit_parms = get_fit_parms('UK', '2013-02-01').ix[field]    

    tau, beta, y0 = fit_parms['tau'], fit_parms['beta'], fit_parms['y0']
    x, y = prepare_xy(prod)
    yfit = y0 * exp(-(x/abs(tau))**beta)
    fit = Series(yfit, index=prod.index) 

    lower_cutoff = '1996-08-01'

    fig = plt.figure(figsize=(w, l))
    ax = fig.gca()

    prod.plot(ax=ax, marker='x', ls='')
    l1 = ax.get_lines()[0]
    l2, = ax.plot(fit[lower_cutoff:].index, fit[lower_cutoff:], '-k')
    
    ax.legend([l1, l2], [field.lower().capitalize() + ' (UK)',
                         r'$y = y0 + exp(-(\frac{t}{\tau})^\beta)$'])

    ax.set_xlabel('Time')
    ax.set_ylabel('Prodction [barrels/day]')

    fig.tight_layout()

    if save:
        os.chdir('article')
        fig.savefig('stretched_exponential.pdf')
        os.chdir('..')
    else:
        plt.show()

def rate_of_discoveries(w=8, l=8, save=False):
    
    fig = plt.figure(figsize=(w, l))
    fig2 = plt.figure(figsize=(w, l))

    rkps_uk = load(open('data/UK_2013_rate.pkl'))
    rkps_no = load(open('data/NO_2013_rate.pkl'))
    
    prod_uk = get_production('UK')
    prod_no = get_production('NO')

    start_of_prod_uk = dict((field, prod_uk[field].dropna().index[0]) for
                                 field in prod_uk)
    start_of_prod_uk = Series(start_of_prod_uk)
    start_of_prod_no = dict((field, prod_no[field].dropna().index[0]) for
                                 field in prod_no)
    start_of_prod_no = Series(start_of_prod_no)

    cats_uk = classify_fields_according_to_urr('UK', '2013-02-01', 'random')
    cats_no = classify_fields_according_to_urr('NO')

    activity_uk = date_range(START['UK'], '2013-02-01', freq='MS')
    n_vs_ts_uk = [] 
    for category in cats_uk:
        starts = array(sorted(start_of_prod_uk[category]))
        n = [(starts <= start).sum() for start in activity_uk]
        t = activity_uk
        n_vs_ts_uk.append((t, n))

    activity_no = date_range(START['NO'], '2013-02-01', freq='MS')
    n_vs_ts_no = [] 
    for category in cats_no:
        starts = array(sorted(start_of_prod_no[category]))
        n = [(starts <= start).sum() for start in activity_no]
        t = activity_no
        n_vs_ts_no.append((t, n))

    small_uk, medium_uk, big_uk = n_vs_ts_uk[0], n_vs_ts_uk[1], n_vs_ts_uk[2]
    small_no, medium_no, big_no = n_vs_ts_no[0], n_vs_ts_no[1], n_vs_ts_no[2]

    ax = fig.add_subplot(311)
    _ax = fig2.add_subplot(111)
    dates_uk = small_uk[0]
    dates_no = small_no[0]
    dates_plot_uk = date_range(START['UK'], '2025-01-01', freq='MS')
    dates_plot_no = date_range(START['NO'], '2025-01-01', freq='MS')
    x1 = array([float(d.toordinal())-START['UK'].toordinal() for d in 
                   dates_plot_uk])
    x2 = array([float(d.toordinal())-START['NO'].toordinal() for d in 
                   dates_plot_no])

    def logi((r, k, p), x):
        return k * p * exp(r * x) / (k + p * (exp(r * x) - 1))

    ax.plot(dates_uk, small_uk[1], 'or')
    ax.plot(dates_plot_uk, logi(rkps_uk[0], x1), '-r')
    
    ax.plot(dates_no, small_no[1], 'xb')
    ax.plot(dates_plot_no, logi(rkps_no[0], x2), '-b')

    l1, = _ax.plot(dates_no, small_no[1], 'xb')
    _ax.plot(dates_plot_no, logi(rkps_no[0], x2), '-b')
#########
    ax2 = fig.add_subplot(312)

    dates_uk = medium_uk[0]
    dates_no = medium_no[0]
    dates_plot_uk = date_range(START['UK'], '2025-01-01', freq='MS')
    dates_plot_no = date_range(START['NO'], '2025-01-01', freq='MS')
    x1 = array([float(d.toordinal())-START['UK'].toordinal() for d in 
                   dates_plot_uk])
    x2 = array([float(d.toordinal())-START['NO'].toordinal() for d in 
                   dates_plot_no])

    def logi((r, k, p), x):
        return k * p * exp(r * x) / (k + p * (exp(r * x) - 1))

    ax2.plot(dates_uk, medium_uk[1], 'or')
    ax2.plot(dates_plot_uk, logi(rkps_uk[1], x1), '-r')
    
    ax2.plot(dates_no, medium_no[1], 'xb')
    ax2.plot(dates_plot_no, logi(rkps_no[1], x2), '-b')

    l2, = _ax.plot(dates_no, medium_no[1], 'sg')
    _ax.plot(dates_plot_no, logi(rkps_no[1], x2), '-g')


########
    ax3 = fig.add_subplot(313)

    dates_uk = big_uk[0]
    dates_no = big_no[0]
    dates_plot_uk = date_range(START['UK'], '2025-01-01', freq='MS')
    dates_plot_no = date_range(START['NO'], '2025-01-01', freq='MS')
    x1 = array([float(d.toordinal())-START['UK'].toordinal() for d in 
                   dates_plot_uk])
    x2 = array([float(d.toordinal())-START['NO'].toordinal() for d in 
                   dates_plot_no])

    def logi((r, k, p), x):
        return k * p * exp(r * x) / (k + p * (exp(r * x) - 1))

    ax3.plot(dates_uk, big_uk[1], 'or')
    ax3.plot(dates_plot_uk, logi(rkps_uk[2], x1), '-r')
    
    ax3.plot(dates_no, big_no[1], 'xb')
    ax3.plot(dates_plot_no, logi(rkps_no[2], x2), '-b')

    l3, = _ax.plot(dates_no, big_no[1], 'or')
    _ax.plot(dates_plot_no, logi(rkps_no[2], x2), '-r')

    fig.tight_layout()
    del fig

    fig2.tight_layout()
    _ax.legend([l1, l2, l3], ['Small fields', 'Medium fields', 'Big fields'],
               loc='upper left')

    _ax.set_xlabel('Time')
    _ax.set_ylabel('Number of Norwegian oil field discovered')

    if save:
        os.chdir('article')
        fig2.savefig('rate_of_discoveries.pdf')
        os.chdir('..')
    else:
        plt.show()

def no_future_2013(w=8, l=10, save=False, **kwargs):
    NUM_REAL = 50
    END_DATE = '2100-01-01'
    f = open('data/no_future_2013_%d.pkl' % NUM_REAL)
    df = load(f)
    f.close()
    
    g = open('hope.pkl')
    multi_parms = load(g)
    g.close()

    tot_prod = df.sum(axis=1) / NUM_REAL

    def doublecycle((qmax1, qmax2, tmax1, tmax2, a1, a2), x):
        return (4 * qmax1 * (exp(-a1*(x-tmax1))) / (1+exp(-a1*(x-tmax1)))**2) +\
               (4 * qmax2 * (exp(-a2*(x-tmax2))) / (1+exp(-a2*(x-tmax2)))**2)

    x = arange(0., len(tot_prod))
    prod_multi = doublecycle(multi_parms['NO']['2013-02-01'], x)
    prod_multi = Series(prod_multi, index=tot_prod.index)

    if 'ax' not in kwargs.keys():
        fig = plt.figure(figsize=(w, l))
        ax = fig.gca()
    else:
        ax = kwargs['ax']

    tot_prod[:'2013-02-01'].plot(ax=ax, marker='o', ls='', color='k')
    prod_multi[:'2013-02-01'].plot(ax=ax, ls='-', color='r') 
    tot_prod['2013-02-01':END_DATE].plot(ax=ax, ls='-', color='b')
    prod_multi['2013-02-01':END_DATE].plot(ax=ax, ls='--', color='r')

    l1, l2, l3, l4 = ax.get_lines()
    ax.legend([l1, l3, l2, l4], ['Data', 'Monte-Carlo forecast', 'Hubbert fit',
        'Hubbert forecast'], loc='upper right')

    print prod_multi['2013-02-01':].sum() / 1e9
    print tot_prod['2013-02-01':].sum() / 1e9

    ax.set_xlabel('Time')
    ax.set_ylabel('Norwegian oil production [barrels/day]')

    if 'ax' not in kwargs.keys():
        fig.tight_layout()

    if save and 'ax' not in kwargs.keys():
        os.chdir('article')
        fig.savefig('no_2013_model_vs_hubbert.pdf')
        os.chdir('..')
    elif not save and 'ax' not in kwargs.keys():
        plt.show()

def uk_future_2013(w=8, l=10, save=False, **kwargs):

    NUM_REAL = 50
    END_DATE = '2100-01-01'
    f = open('data/uk_future_2013_%d.pkl' % NUM_REAL)
    df = load(f)
    f.close()
    
    g = open('hope.pkl')
    multi_parms = load(g)
    g.close()

    tot_prod = df.sum(axis=1) / NUM_REAL

    def doublecycle((qmax1, qmax2, tmax1, tmax2, a1, a2), x):
        return (4 * qmax1 * (exp(-a1*(x-tmax1))) / (1+exp(-a1*(x-tmax1)))**2) +\
               (4 * qmax2 * (exp(-a2*(x-tmax2))) / (1+exp(-a2*(x-tmax2)))**2)

    x = arange(0., len(tot_prod))
    prod_multi = doublecycle(multi_parms['UK']['2013-02-01'], x)
    prod_multi = Series(prod_multi, index=tot_prod.index)

    if 'ax' not in kwargs.keys():
        fig = plt.figure(figsize=(w, l))
        ax = fig.gca()
    else:
        ax = kwargs['ax']

    tot_prod[:'2013-02-01'].plot(ax=ax, marker='o', ls='', color='k')
    prod_multi[:'2013-02-01'].plot(ax=ax, ls='-', color='r') 
    tot_prod['2013-02-01':END_DATE].plot(ax=ax, ls='-', color='b')
    prod_multi['2013-02-01':END_DATE].plot(ax=ax, ls='--', color='r')

    l1, l2, l3, l4 = ax.get_lines()
    ax.legend([l1, l3, l2, l4], ['Data', 'Monte-Carlo forecast', 'Hubbert fit',
        'Hubbert forecast'], loc='upper right')

    print prod_multi['2013-02-01':].sum() / 1e9
    print tot_prod['2013-02-01':].sum() / 1e9

    ax.set_xlabel('Time')
    ax.set_ylabel('UK oil production [barrels/day]')

    if 'ax' not in kwargs.keys():
        fig.tight_layout()

    if save and 'ax' not in kwargs.keys():
        os.chdir('article')
        fig.savefig('uk_2013_model_vs_hubbert.pdf')
        os.chdir('..')
    elif not save and 'ax' not in kwargs.keys():
        plt.show()

def uk_and_no_2013(w=8, l=15, save=False):
    fig = plt.figure(figsize=(w, l))
    ax = fig.add_subplot(211)
    no_future_2013(ax=ax)
    ax.set_xlabel('')
    ax2 = fig.add_subplot(212)
    uk_future_2013(ax=ax2)

    fig.tight_layout()

    if save:
        os.chdir('article')
        fig.savefig('no_and_uk_2013.pdf')
        os.chdir('..')
    else:
        plt.show()

def no_bt_2003(w=8, l=10, save=False, **kwargs):
    NUM_REAL = 50
    END_DATE = '2100-01-01'
    f = open('data/no_future_2003_%d.pkl' % NUM_REAL)
    df = load(f)
    f.close()
    
    g = open('hope.pkl')
    multi_parms = load(g)
    g.close()

    tot_prod = df.sum(axis=1) / NUM_REAL

    def doublecycle((qmax1, qmax2, tmax1, tmax2, a1, a2), x):
        return (4 * qmax1 * (exp(-a1*(x-tmax1))) / (1+exp(-a1*(x-tmax1)))**2) +\
               (4 * qmax2 * (exp(-a2*(x-tmax2))) / (1+exp(-a2*(x-tmax2)))**2)

    x = arange(0., len(tot_prod))
    prod_multi = doublecycle(multi_parms['NO']['2003-02-01'], x)
    prod_multi = Series(prod_multi, index=tot_prod.index)

    if 'ax' not in kwargs.keys():
        fig = plt.figure(figsize=(w, l))
        ax = fig.gca()
    else:
        ax = kwargs['ax']

    tot_prod[:'2003-02-01'].plot(ax=ax, marker='o', ls='', color='k')
    prod_multi[:'2003-02-01'].plot(ax=ax, ls='-', color='r') 
    tot_prod['2003-02-01':END_DATE].plot(ax=ax, ls='-', color='b')
    prod_multi['2003-02-01':END_DATE].plot(ax=ax, ls='--', color='r')

    prod_2003_2013 = get_production('NO').sum(axis=1)['2003-02-01':].dropna()
    prod_2003_2013.plot(ax=ax, marker='x', ls='', color='k')

    l1, l2, l3, l4, l5 = ax.get_lines()
    ax.legend([l1, l5, l3, l4], ['Data up to 2003', 
        'Data from 2003 to 2013', 'Monte-Carlo forecast',
        'Hubbert forecast'], loc='upper right')

    print prod_multi['2013-02-01':].sum() / 1e9
    print tot_prod['2013-02-01':].sum() / 1e9

    ax.set_xlabel('Time')
    ax.set_ylabel('Norwegian oil production [barrels/day]')

    if 'ax' not in kwargs.keys():
        fig.tight_layout()

    if save and 'ax' not in kwargs.keys():
        os.chdir('article')
        fig.savefig('no_2003_model_vs_hubbert.pdf')
        os.chdir('..')
    elif not save and 'ax' not in kwargs.keys():
        plt.show()


def uk_bt_1998(w=8, l=10, save=False, **kwargs):
    NUM_REAL = 50
    END_DATE = '2100-01-01'
    f = open('data/uk_future_1998_%d.pkl' % NUM_REAL)
    df = load(f)
    f.close()
    
    g = open('hope.pkl')
    multi_parms = load(g)
    g.close()

    tot_prod = df.sum(axis=1) / NUM_REAL

    def doublecycle((qmax1, qmax2, tmax1, tmax2, a1, a2), x):
        return (4 * qmax1 * (exp(-a1*(x-tmax1))) / (1+exp(-a1*(x-tmax1)))**2) +\
               (4 * qmax2 * (exp(-a2*(x-tmax2))) / (1+exp(-a2*(x-tmax2)))**2)

    x = arange(0., len(tot_prod))
    prod_multi = doublecycle(multi_parms['UK']['1998-02-01'], x)
    prod_multi = Series(prod_multi, index=tot_prod.index)

    if 'ax' not in kwargs.keys():
        fig = plt.figure(figsize=(w, l))
        ax = fig.gca()
    else:
        ax = kwargs['ax']

    tot_prod[:'1998-02-01'].plot(ax=ax, marker='o', ls='', color='k')
    prod_multi[:'1998-02-01'].plot(ax=ax, ls='-', color='r') 
    tot_prod['1998-02-01':END_DATE].plot(ax=ax, ls='-', color='b')
    prod_multi['1998-02-01':END_DATE].plot(ax=ax, ls='--', color='r')

    prod_1998_2013 = get_production('UK').sum(axis=1)['1998-02-01':].dropna()
    prod_1998_2013.plot(ax=ax, marker='x', ls='', color='k')

    l1, l2, l3, l4, l5 = ax.get_lines()
    ax.legend([l1, l5, l3, l4], ['Data up to 2003', 
        'Data from 2003 to 2013', 'Monte-Carlo forecast',
        'Hubbert forecast'], loc='upper right')

    print prod_multi['2013-02-01':].sum() / 1e9
    print tot_prod['2013-02-01':].sum() / 1e9

    ax.set_xlabel('Time')
    ax.set_ylabel('UK oil production [barrels/day]')

    if 'ax' not in kwargs.keys():
        fig.tight_layout()

    if save and 'ax' not in kwargs.keys():
        os.chdir('article')
        fig.savefig('uk_1998_model_vs_hubbert.pdf')
        os.chdir('..')
    elif not save and 'ax' not in kwargs.keys():
        plt.show()


def uk_and_no_bt(w=8, l=10, save=False):
    fig = plt.figure(figsize=(w, l))
    ax = fig.add_subplot(211)
    no_bt_2003(ax=ax)
    ax.set_xlabel('')
    ax2 = fig.add_subplot(212)
    uk_bt_1998(ax=ax2)

    fig.tight_layout()

    if save:
        os.chdir('article')
        fig.savefig('no_and_uk_bt.pdf')
        os.chdir('..')
    else:
        plt.show()


