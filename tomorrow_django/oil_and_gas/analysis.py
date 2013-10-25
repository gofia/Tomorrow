from constants import MIN_PROD
from constants import M3_TO_BARRELS
from constants import START
from constants import BOUNDS
from constants import MAX_DATE
from fitting import fit_exponential
from fitting import fit_stretched_exponential
from fitting import fit_power_law
from fitting import prepare_xy
from get_data import get_production
from get_data import get_classification
from config import DPATH

from fit_logistic import fit_logistic
from fit_logistic import compute_logistic

from pandas import date_range, concat, Series, DataFrame, Timestamp
from pandas.tseries.offsets import *

from numpy import array, exp, log, sign, arange, log10, ceil, inf
from numpy.random import choice
from numpy.random import rand 

from pickle import load, dump

import matplotlib.pyplot as plt

import os

def get_fit_parms(country, until='2013-02-01', 
    fit_style='stretched exponential', xmin='my_xmin'):
    """Return a DataFrame with the fields as the index and name of the relevant 
    fit parameters as columns.

    Args:
        country -> str.
            The string representing the name of the country.
        until -> str.
            The string representing the date until which we take the monthly
            oil production into account. This is especially useful for 
            backtesting.
        fit_style -> str.
            The string representing the fit style.
        xmin -> str.
            The string representing the x-coordinate of the production 
            timeseries from which the fitting is done.

    Return:
        fit_parms -> DataFrame.
            The DataFrame containing the fit parameters. 
    """
    
    fit_parms = {}
    if fit_style == 'exponential':
        fit = fit_exponential
        columns = ['tau', 'y0']
    elif fit_style == 'stretched exponential':
        fit = fit_stretched_exponential
        columns = ['tau', 'beta', 'y0']
    elif fit_style == 'power law':
        fit = fit_power_law
        columns = ['alpha', 'y0']

    fpath = os.path.join(DPATH, '%s_fit_parms_%s_%s' % (country, until[:4], 
                fit_style[:2]))

    if os.path.exists(fpath):
        f = open(fpath)
        fit_parms = load(f)
        f.close()
        return fit_parms

    production = get_production(country, until)
    classification = get_classification(country, until)
    #Returns the fields that are regular (and thus fittable)
    fields = classification[classification['regular']].index

    #We define get_xmin, a function that returns the "left cutoff value" for the
    #fits.
    if xmin == 'my_xmin':
        def get_xmin(field):
            field_xmin = classification.ix[field]['from']
            return field_xmin

    #Filling the fit_parms DataFrame
    fit_parms = DataFrame(index=fields, columns=columns)
    for field in fields:
        fit_parms.ix[field] = fit(production[field], xmin=get_xmin(field))

    f = open(fpath, 'w')
    dump(fit_parms, f)
    f.close()
    return fit_parms

def _extend_production(_prod, fit_parm, fit_style='stretched exponential'):
    """Extend the production of a given oil field into the future, given the
    fit_parms and the fit_style.

    Args:
        _prod -> Series.
            The time series of production of a given field.
        fit_parm -> tuple.
            The fit parameters for the particular field. Ex: (tau, beta, y0)
        fit_style -> str.
            The string representing the fit style.

    Return:
        _extended_prod -> Series.
            The time series of the extended production (past + future) of the
            field.
    """
    #_prod is a time series of production i.e. the production of an individual
    #field
    extension_start = _prod.index[-1] + MonthBegin()
    extraction_start = _prod.dropna().index[0]

    if fit_style == 'stretched exponential':
        tau, beta, yo = fit_parm
        #The number of days until the production reaches MIN_PROD since the 
        #beginning of the extraction.
        lifetime = abs(tau) * (-log(MIN_PROD/yo)) ** (1./beta)
        #Timestamp don't extend beyond 2262-04-11
        max_lifetime = (MAX_DATE - extraction_start).days
        lifetime = min(lifetime, max_lifetime)
    elif fit_style == 'power-law':
        print 'power-law not implemented yet for extend_production()'
        1/0
    extension_end = extraction_start + lifetime * Day()
    #we round end down to the beginning of the month (so that we stay for sure
    #with end < 2262-04-11
    extension_end = MonthBegin().rollback(extension_end)
    future = date_range(extension_start, extension_end, freq='MS')

    nfuture = len(future)
    #Are we already very close (or below) MIN_PROD?
    if nfuture == 0:
        return _prod
           
    #subtlety: I need to initialize _extended_prod with something for the 
    #extended part (in this case 42). Else, the whole extended part will be 
    #dropped in prepare_xy.
    _extended_prod = concat((_prod, Series(nfuture*[42], index=future, 
                             name=_prod.name)))
    x, y = prepare_xy(_extended_prod)
    if fit_style == 'stretched exponential':
        #overwriting the placeholder (nfuture*[42])
        y = yo * exp(sign(tau) * (x[-nfuture:] / abs(tau))**beta)
        _extended_prod[-nfuture:] = y

    return _extended_prod

def extend_production(country, until='2013-02-01', 
    fit_style='stretched exponential', xmin='my_xmin'):
    """Extends the production of the different oil fields into the future, given
    the fit style.

    Args:
        country -> str
            The string representing the country we are dealing with. Ex: 'NO'
        until -> str
            The datetime like string used for backtesting.
        fit_style -> str
            The string representing the fit style.
        xmin -> str
            The choice for the "left cutoff" when fitting.

    Return:
        extended_prod -> DataFrame
            The DataFrame of the extended production.
    """
    fpath = os.path.join(DPATH, '%s_extended_%s_%s' % (country, until[:4], 
                fit_style[:2]))
    if os.path.exists(fpath):
        f = open(fpath)
        extended_production = load(f)
        f.close()
        return extended_production

    production = get_production(country=country, until=until)
    classification = get_classification(country=country, until=until)
    fields = classification[classification['regular']].index
    fit_parms = get_fit_parms(country=country, until=until, fit_style=fit_style,
                    xmin=xmin)

    extended_productions = []
    for field in fields:
        _prod = production[field]
        _extended_prod = _extend_production(_prod, fit_parms.ix[field], 
            'stretched exponential')
        extended_productions.append(_extended_prod)

    f = open(fpath, 'w')
    extended_production = concat(extended_productions, axis=1)
    dump(extended_production, f)
    f.close()
    return extended_production

def logistic_extrap(country, field, until, start, cutoff, k_frac):
    """Extrapolates the the logistic fit of a field from start, only taking
    data from cutoff into account, until the fit reaches k_frac * k.
    """
    prod = get_production(country, until)[field].dropna()[cutoff:]
    x, y = prod.index, prod.values
    nx = len(x)

    fname = os.path.join(DPATH, 
                '%s_logistic_production_%s.pkl' % (country, until[:4]))
    if os.path.exists(fname):
        f = open(fname)
        rkp_dict = load(f)
        f.close()
        r, k, p = rkp_dict[field]
    else:
        r, k, p = fit_logistic(x, y, Timestamp(start))
 

    if y[-1] > k_frac * k:
        return (x, y)

    while y[-1] < k_frac * k:
        x = list(x)
        last_date = x[-1]
        future = date_range(last_date, periods=120, freq='MS')[1:]
        x.extend(future)
        y = compute_logistic(x, (r, k, p), Timestamp(start))

    _y = y[nx:]
    _y = _y[_y < k_frac * k]
    _x = x[nx:]
    _x = _x[:len(_y)]

    return (_x, _y)

def extend_the_bad_ones(country, until='2013-02-01', style='urr',
    fit_style='stretched exponential', xmin='my_xmin'):
    """Extends the production of the irregular/insufficient oil fields into the
    future, given the fit style.

    Args:
        country -> str
            The string representing the country we are dealing with. Ex: 'NO'
        until -> str
            The datetime like string used for backtesting.
        style -> str
            The style used for the extension. Ex: 'random', 'urr'
        fit_style -> str
            The string representing the fit style.
        xmin -> str
            The choice for the "left cutoff" when fitting.

    Return:
        extended_prod -> DataFrame
            The DataFrame of the extended production.
    """
    ###A big mess was created with is_logistic... Taking into account the 
    ###possibility of future rise of oil_production of irregular fields.

    #No URR data for UK
    if country == 'UK':
        assert style == 'random'

    production = get_production(country=country, until=until)
    classification = get_classification(country=country, until=until)
    fields = classification[classification['bad']].index
 
    if style == 'random':
        fname = os.path.join(DPATH, '%s_logistic_extension_%s.pkl' % (
                country, until[:4]))
        f = open(fname)
        logistic_start = load(f)
        f.close()
        #The "good fields" i.e. those who are regular enough for a fit. We will
        #sample the decay for our "bad fields" from the good ones.
        _extended_production = extend_production(country, until, fit_style,
                                   xmin)
        samples = choice(_extended_production.columns, len(fields))
        ss = []
        for field, sample in zip(fields, samples):
            is_logistic = False
            if field in logistic_start.keys():
                if_logistic = True
                start = logistic_start[field][0]
                cutoff = logistic_start[field][1]
                x, y = logistic_extrap(country, field, until, start, cutoff, 0.95)
            if is_logistic:
                tail_shape = _extended_production[sample][until:][1:].values
                tail = list(y) + list(y[-1]/tail_shape[0] * tail_shape)
                idx = _extended_production[until:][1:].index
                nmax = len(idx)
                tail = tail[:nmax]
                ntail = len(tail)
                tail = Series(tail, index=idx[:ntail], name=field)
            else:
                tail_shape = _extended_production[sample][until:][1:]
                #We need to scale the tail_shape to the field we want to extend.
                tail = production[field].dropna()[-1]/tail_shape[0] * tail_shape
                tail.name = field
            ss.append(tail)
            is_logistic = False
        future_prod = concat(ss, axis=1)
        extended_prod = concat((production[fields], future_prod))

        return extended_prod

    if style == 'urr':
        urr_estimates = classification['urr'].ix[fields] 
        if country == 'NO':
            urr_estimates *= 1e6 * M3_TO_BARRELS
        fname = os.path.join(DPATH, '%s_logistic_extension_%s.pkl' % (
                country, until[:4]))
        f = open(fname)
        logistic_start = load(f)
        f.close()

        ss = []
        for field in fields:
            prod_until_now = production[field].sum()
            prod_remaining = urr_estimates[field] - prod_until_now
            prod_now = production[field].dropna()[-1]

            is_logistic = False
            if field in logistic_start.keys():
                is_logistic = True
                start = logistic_start[field][0]
                cutoff = logistic_start[field][1]
                x, y = logistic_extrap('NO', field, until, 
                           logistic_start[field][0], logistic_start[field][1],
                           0.95)
                prod_now = y[-1]
                prod_remaining -= sum(y)            

           #comes from the constraint that sum over future equals remaining
            tau = prod_remaining / prod_now
            #time from start in months.
            if is_logistic:
                tnow = len(production[field].dropna()) + len(y)
            else:
                tnow = len(production[field].dropna())

            #comes from the constraint that p(tnow) = pnow
            y0 = prod_now * exp(tnow/tau)

            if is_logistic:
                lifetime = -tau * log(MIN_PROD/y0) + len(y)
            else:
                lifetime = -tau * log(MIN_PROD/y0)
            
            max_nfuture_months = 12 * (MAX_DATE.year - Timestamp(until).year) +\
                                      (MAX_DATE.month - Timestamp(until).month)
            if is_logistic:
                nfuture_months = min(max_nfuture_months, max(0, 
                    int(lifetime-tnow)+len(y)))
            else:
                nfuture_months = min(max_nfuture_months, 
                                     max(0, int(lifetime-tnow)))
       
            if nfuture_months == 0:
                ss.append(production[field])
                continue
            future = date_range(Timestamp(until) + MonthBegin(), 
                         periods=nfuture_months, freq='MS')
            if is_logistic:
                ly = list(y)
                ly.extend(y0 * exp(-arange(tnow+1, tnow+1+nfuture_months-len(y))/tau))
                prod_future = array(ly)
            else:
                prod_future = y0 * exp(-arange(tnow+1, tnow+1+nfuture_months)/tau)
            ss.append(Series(prod_future, index=future, name=field, dtype='float64'))
            is_logistic = False
        future_prod = concat(ss, axis=1)
        extended_prod = concat((production[fields], future_prod))
       
        return extended_prod

    if style == 'const':
        urr_estimates = classification['urr'].ix[fields]
        if country == 'NO':
            urr_estimates *= 1e6 * M3_TO_BARRELS
        ss = []
        for field in fields:
            prod_until_now = production[field].sum()
            prod_remaining = urr_estimates[field] - prod_until_now
            prod_now = production[field].dropna()[-5:].mean()
            n = prod_remaining / prod_now
            max_nfuture_months = 12 * (MAX_DATE.year - Timestamp(until).year) +\
                                      (MAX_DATE.month - Timestamp(until).month)
            nfuture_months = min(max_nfuture_months, max(0, int(n)))
 
            if nfuture_months == 0:
                ss.append(production[field])
                continue
            future = date_range(Timestamp(until) + MonthBegin(), 
                         periods=nfuture_months, freq='MS')
            prod_future = len(future) * [prod_now]
            ss.append(Series(prod_future, index=future, name=field))
        future_prod = concat(ss, axis=1)
        extended_prod = concat((production[fields], future_prod)) 

        return extended_prod

def extend_all(country, until='2013-02-01', fit_style='stretched exponential',
    style='urr', xmin='my_xmin'):
    """Extends the production of all fields (regular, irregular, inactive and
    insufficient) and returns the results in single DataFrame.
    
     Args:
        country -> str
            The string representing the country we are dealing with. Ex: 'NO'
        until -> str
            The datetime like string used for backtesting.
        fit_style -> str
            The string representing the fit style.
        style -> str
            The style used for the extension of "bad" fields. Ex: 'random','urr'
        xmin -> str
            The choice for the "left cutoff" when fitting.

    Return:
        extended_prod -> DataFrame
            The DataFrame of the extended production.
    """
    regulars = extend_production(country, until, fit_style, xmin)
    bad_ones = extend_the_bad_ones(country, until, style, fit_style, xmin)
    production = get_production(country, until)
    classification = get_classification(country, until)
    fields = classification[classification['inactive']]['inactive'].index
    inactives = production[fields]
    extended_prod = concat((regulars, bad_ones, inactives), axis=1).sort(axis=1)

    return extended_prod

def perturb_fit_parms(country, until='2013-02-01', 
    fit_style='stretched exponential', xmin='my_xmin', perturbation=0.1, 
    step=0.01, parm_names=['tau', 'beta']):
    """We perturb the parameters of the fit and look at the impact on the cost
    function.

    Args:
        country -> str
            The string representing the country.
        until -> str
            The datelike string used for backtesting.
        fit_style -> str
            The string representing the fitting style.
        xmin -> str
            The choice for the "left cutoff" when fitting.
        perturbation -> float
            The percentage with which the fit parameters are perturbated.
        step -> float
            The resolution of the perturbation.
        parm_names -> list
            The name of the parameters we wish to perturb.

    Return:
        res -> tuple of lists
            Each list represents 
    """
    fit_parms = get_fit_parms(country=country, until=until, fit_style=fit_style,
                    xmin=xmin)
    production = get_production(country, until)
    changes = arange(1.-perturbation, 1+perturbation+step, step)
    res = {}
    print 'It will be implemented later.'

def urr_vs_urr(country, until='2013-02-01', fit_style='stretched exponential'):
    """Returns the DataFrame containing our estimate of the ultimate recoverable
    resources (URR) and the official estimate.

    Args:
        country -> str
            The country of the oil fields.
        until -> str
            The datelike string for the "left cutoff".

    Return:
        urrs -> DataFrame
            The DataFrame containing our and the official estimates of the URR.
    """
    assert country != 'UK', 'UK has no official URR estimate!'

    extended_production = extend_production(country, until=until, 
                              fit_style=fit_style, xmin='my_xmin')
    our_urrs = extended_production.sum()
    our_urrs.name = 'ours'
    classification = get_classification(country, until)
    their_urrs = classification.ix[our_urrs.index]['urr']
    their_urrs = 1e6 * M3_TO_BARRELS * Series(their_urrs, name='theirs')

    return concat((our_urrs, their_urrs), axis=1)
 
def classify_fields_according_to_urr(country, until='2013-02-01', style='urr'):
    """Returns a list of list of fields according to the classification
    based on their URR.
    """
    bounds = BOUNDS[country][until]
    bins = []
    lower_bound = 0.
    for bound in bounds:
        bins.append((lower_bound, bound))
        lower_bound = bound
    bins.append((bound, inf))

    if not style == 'urr':
        urrs = extend_all(country, until, style=style).sum()
    else:
        cls = get_classification(country, until)
        urrs = cls['urr'] * 1e6 * M3_TO_BARRELS
    categories = []
    for bin in bins:
        fields = urrs[(urrs > bin[0]) & (urrs < bin[1])].index 
        categories.append(fields)

    return categories   
   
def rate_of_discoveries(country, until='2013-02-01', fit_style='logistic', 
    confid=None, show_plot=False, style='urr'):
    """Fits a logistic curve to the number of fields discovered up to time t. 
    This informs us about the underlying discovery mechanism. This mechanism can
    depend on size.

    Args:
        country -> str:
            The string representing the name of the country.
        until -> str:
            datelike string useful for backtesting (left cutoff)

    Return:
        discoveries -> DataFrame:
            DataFrame containing all the discoveries.

    """
    production = get_production(country, until)
    fields = production.columns
    start_of_prod = dict((field, production[field].dropna().index[0]) for 
                          field in fields)
    start_of_prod = Series(start_of_prod)
    categories = classify_fields_according_to_urr(country, until, style)
    
    activity = date_range(START[country], until, freq='MS')
    n_vs_ts= []
    for category in categories:
        starts = array(sorted(start_of_prod[category]))
        n = [(starts <= start).sum() for start in activity]
        t = activity
        n_vs_ts.append((t, n))
 
    #return n_vs_ts
    fit_params = []
    fname = os.path.join(DPATH, '%s_%s_rate.pkl' % (country, until[:4]))
    if os.path.exists(fname):
        f = open(fname)
        rkp_dict = load(f)
        f.close()
    for i, n_vs_t in enumerate(n_vs_ts):
        x, y = n_vs_t[0], n_vs_t[1]
        if os.path.exists(fname):
            (r, k, p) = rkp_dict[i]
        else:
            #res = fit_logistic(x, y, START[country], confid, show_plot)
            (r, k, p) = fit_logistic(x, y, START[country], confid, show_plot)
        fit_params.append((r, k, p))
    
    return fit_params
    
#def correct_fit_parms(urrs, fit_parms, tolerance=1.5, 
#                      conv=1.1):
#    """If the urr we get from our extrapolation is bigger or smaller than the
#    official urr by the tolerance factor, we change the beta of the fit_parms
#    until the newly computed urr falls within some limits set by convergence.
#    """
#    #hack
#    fit_parms, oil_fields = fit_parms
#    #Doesn't work. Maybe bug: it thinks that the key is a list (not allowed)
#    #however, only my values are list (allowed)
#    #fit_parms = {(k, list(v)) for k, v in fit_parms.items()}
#    fps = {}
#    for k, v in fit_parms.items():
#        fps[k] = list(v)
#    fit_parms = fps
#    ours = urrs['ours']
#    theirs = urrs['theirs']
#
#    black_sheep = urrs[(ours/theirs >= tolerance) |
#                       (ours/theirs <= 1./tolerance)].index
#    step = dict(zip(black_sheep, [1.1]*len(black_sheep)))
#    for sheep in black_sheep:
#        factor_before = 1. if ours[sheep] > theirs[sheep] else -1.
#        while True:
#            if factor_before == 1:
#                fit_parms[sheep][1] *= step[sheep]
#            else:
#                fit_parms[sheep][1] /= step[sheep]
#            new_urr = extend_production(oil_fields[sheep], 
#                          fit_parms[sheep]).sum()
#            print ' sheep: %s \n beta: %s\n new urr: %s\n target: %s\n\n' %\
#                (sheep, fit_parms[sheep][1], new_urr, new_urr/theirs[sheep])
#            if (new_urr < theirs[sheep] * conv) and\
#               (new_urr > theirs[sheep] / conv):
#                break
#            factor_after = 1. if new_urr >= theirs[sheep] else -1.
#            if factor_after == factor_before:
#                continue
#            else:
#                step[sheep] = (step[sheep] - 1.) * 0.5 + 1.
#                #print 'step: %s' % step[sheep]
#            factor_before = factor_after
#    fit_parms = dict((k, tuple(v)) for k, v in fit_parms.items())
#
#    return (fit_parms, oil_fields)
#
def thinning((r, k, p0), t, country):
    """Implemenation of the thinning method used to generate an inohomogenous 
    Poisson process. The method assumes that lamda behaves like rp(1-p/k)
    """ 
    r *= 30    #day -> month
    lamda_max = r*k / 4
    dt = -log(rand(1)) / lamda_max
    try:
        t_next = (t + dt * MonthBegin())[0]
    except:
        return (MAX_DATE, False)

    nmonths = len(date_range(START[country], t_next, freq='MS')) 
    p_next = k*p0*exp(r*nmonths) / (k + p0*(exp(r*nmonths))-1)
    lamda_next = r*p_next * (1 - p_next/k)
    accepted = (lamda_max * rand(1) < lamda_next)[0]

    return (t_next, accepted)

def oracle(country, until='2013-02-01', style='urr', confid=None):
    """The oracle predicts the future oil production of a given country.
    """

    extended_production = extend_all(country, until, style=style)
    categories = classify_fields_according_to_urr(country, until, style=style)
    rates = rate_of_discoveries(country, until, confid=confid, style=style)    
    t = Timestamp(until)

    ntot = len(extended_production[until:])

    last_index = extended_production.index[-1]
    new_prods = []
    percents = [0]
    for i, rate in enumerate(rates):
        count=0
        print 'Category %s:\n    ' %i,
        while t < MAX_DATE:
            r, k, p = rate
            t_next, accepted = thinning((r, k, p), t, country)
            t = t_next

            _n = len(extended_production[t:])
            percent = 100 - 100*_n/ntot
            if (percents[-1] != percent) and (percent%10==0):            
               percents.append(percent)
               print '%s%%' %percent,

            if not accepted:
                continue

            picked = choice(categories[i])[0]
            new_prod = extended_production[picked]
            #it might have been simpler to .dropna() the previous line. But
            #there can be holes in the data.
            start_new_prod = new_prod.dropna().index[0]
            new_prod = new_prod[start_new_prod:].values
            n = len(extended_production[t:])
            idx = extended_production.index
            s = Series(index=idx)
            s[t:] = new_prod[:n]
            s.name = 'field%s__%s' % (i, count)
            new_prods.append(s)
            count += 1
        t = Timestamp(until)
        print '\n'
    new_prods = concat(new_prods, axis=1)
    return concat((extended_production, new_prods), axis=1)    
 

##    'medium': all_extended_fields.sum()[(log10(all_extended_fields.sum()) >= 
##                  6.0) & (log10(all_extended_fields.sum()) < 7.0)],
##    'big': all_extended_fields.sum()[log10(all_extended_fields.sum()) >= 7.0]
##        }
#
#    fields = {
#    'small': all_extended_fields.sum()[log10(all_extended_fields.sum()) < 7.],
#    'big': all_extended_fields.sum()[log10(all_extended_fields.sum() >= 7.)],
#        }
#
##    today = Timestamp('02-01-2013')
#    today = Timestamp('02-01-2003')
#    t = today
#    scenario = all_extended_fields.copy()
#    #return scenario
#    rkp = {'small': (rs, ks, ps), 'medium': (rm, km, pm), 'big': (rb, kb, pb)}
#    for field_size in ('small', 'big'):#('small', 'medium', 'big'):
#        t = today
#        i = 1
#        while t < Timestamp('01-01-2260'):
#            t_next, accepted = thinning(rkp[field_size], t)
#            t = t_next
#            if t >= Timestamp('01-01-2260'):
#                t = today
#                break
#            if accepted:
#                picked = choice(fields[field_size].index)[0]
#                start = all_extended_fields[picked].dropna().index[0]
#                end = all_extended_fields[picked].dropna().index[-1]
#                dt = list(all_extended_fields.index).index(t) -\
#                    list(all_extended_fields.index).index(start)
#                if (Timestamp('01-01-2260') - end).days >= dt * 30:
#                    df = DataFrame(all_extended_fields[picked].dropna().\
#                         shift(dt, freq='MS'), 
#                         columns=['%s_%s' % (field_size, i)])
#                    scenario = concat((scenario, df), axis=1)
#                    _df = DataFrame(all_extended_fields[picked].dropna(),
#                              columns=['%s__%s' % (field_size, i)])
#                else:
#                    cutoff_id = dt * 30 - (Timestamp('01-01-2260') - end).days
#                    cutoff_id = ceil(cutoff_id / 30.)           
#                    scenario = concat((scenario, 
#                       DataFrame(all_extended_fields[picked][:-cutoff_id].dropna().shift(dt, freq='MS'), columns=['%s_%s' % (field_size, i)])), axis=1)
#                i += 1 
#    return scenario
#
