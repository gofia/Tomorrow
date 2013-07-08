from constants import GOOD_FITS
from constants import BAD_FITS
from constants import MAXES
from constants import MIN_PROD
from constants import URRS
from constants import M3_TO_BARRELS
from constants import START
from constants import END
from fitting import fit_exponential
from fitting import fit_stretched_exponential
from fitting import fit_power_law
from fitting import prepare_xy
from fitting import chop_xy
from fitting import cost_function
from fitting import xmin2xmin
from get_data import get_oil_fields

from pandas import date_range
from pandas.tseries.offsets import *
from pandas.tseries.offsets import DateOffset
from pandas import concat
from pandas import Series
from pandas import DataFrame
from pandas import Timestamp

from numpy import array
from numpy import exp
from numpy import log
from numpy import sign
from numpy import arange
from numpy import log10
from numpy import ceil
from numpy.random import choice
from numpy.random import rand 

import matplotlib.pyplot as plt

def get_fit_parms(fields=GOOD_FITS, fit_style='stretched exponential', 
    xmin='custom', return_oil_field=True):
    """Return a hash with the keys being the fields (names) and value the 
    relevant fit parameters given the fit style.
    """
    fit_parms = {}
    if fit_style == 'exponential':
        fit = fit_exponential
    elif fit_style == 'stretched exponential':
        fit = fit_stretched_exponential
    elif fit_style == 'power law':
        fit = fit_power_law

    oil_fields = get_oil_fields()

    if xmin == 'custom':
        def get_xmin(field, MAXES):
            return MAXES[field] if field in MAXES.keys() else 'max'

    for field in fields:
        fit_parms[field] = fit(oil_fields[field], xmin=get_xmin(field, MAXES))

    if return_oil_field:
        return (fit_parms, oil_fields)
    else:
        return fit_parms


def extend_production(oil_field, fit_parms, fit_style='stretched exponential'):
    """Extend the production of a given oil field into the future, given the
    fit_parms and the fit_style.
    """
    start = oil_field.index[-1] + MonthBegin()
    if fit_style == 'stretched exponential':
        tau, beta, yo = fit_parms
        lifetime = abs(tau) * (-log(MIN_PROD/yo)) ** (1./beta)
    try:
        end = oil_field.dropna().index[0] + lifetime * Day()
    except:
        lifetime = 200 * 365 if lifetime > 200 * 365 else lifetime
        end = oil_field.dropna().index[0] + lifetime * Day()
    end = MonthBegin().rollback(end) + DateOffset(months=1)
    future = date_range(start, end, freq='MS')

    nfuture = len(future)
    if nfuture == 0:
        return oil_field
           
    oil_field = concat((oil_field, Series(len(future) * [1], index=future,
        name=oil_field.name)))
    x, y = prepare_xy(oil_field)
    if fit_style == 'stretched exponential':
        y = yo * exp(sign(tau) * (x[-nfuture:] / abs(tau))**beta)
        oil_field[-nfuture:] = y

    return oil_field

def extend_productions(fields=GOOD_FITS, fit_parms='None', 
    fit_style='stretched exponential', xmin='custom', freq='M'):
    """Extends the production of the different oil fields into the future, given
    the fit style.
    """
    if fit_parms == 'None':
        fit_parms, oil_fields = get_fit_parms(fields=fields, 
            fit_style=fit_style, xmin=xmin)
    else:
        fit_parms, oil_fields = fit_parms
    extensions = []
    for field in fields:
        oil_field = oil_fields[field]
        oil_field = extend_production(oil_field, fit_parms[field], 
            'stretched exponential')
        start = oil_field.index[-1] + MonthBegin()
        tau, beta, yo = fit_parms[field]
        lifetime = abs(tau) * (-log(MIN_PROD/yo)) ** (1./beta)
        try:
            end = oil_field.dropna().index[0] + lifetime * Day()
        except:
            end = Timestamp('01-01-2260')
        end = MonthBegin().rollback(end) + DateOffset(months=1)
        future = date_range(start, end, freq='MS')
        
        nfuture = len(future)
        if nfuture == 0:
            extensions.append(oil_field)
            continue
        oil_field = concat((oil_field, Series(len(future) * [1], index=future,
            name=oil_field.name)))
        x, y = prepare_xy(oil_field)
        #from erpy.ipshell import ipshell
        #ipshell('')
        if fit_style == 'stretched exponential':
            y = yo * exp(sign(tau) * (x[-nfuture:] / abs(tau))**beta)
            oil_field[-nfuture:] = y
        extensions.append(oil_field)

    return concat(extensions, axis=1)

def perturb_fit_parms(fields=GOOD_FITS, fit_style='stretched exponential',
    xmin='custom', perturbation=0.1, step=0.01):
    """We perturb the parameters of the fit and look how flat the cost_function
    is. We will see how much perturbation the parameters can take for a fixed 
    difference in the value of the cost function (ex: 10%). Or the reverse: fix
    the parms and look how the cost function varies.
    """
    (fit_parms, oil_fields) = get_fit_parms(fields=fields, fit_style=fit_style,
        xmin=xmin)    
    def get_xmin(field, MAXES):
        return MAXES[field] if field in MAXES.keys() else 'max'

    res = {}
    for field_name in fit_parms.keys():
        tau, beta, yo = fit_parms[field_name]
        changes = arange(1.-perturbation, 1+perturbation+step, step)
        taus = changes * tau
        betas = changes * beta
        xs, ys, zs = [], [], []
        for tau in taus:
            for beta in betas:
                xs.append(tau)
                ys.append(beta)
                _x, _y = oil_fields[field_name], None
                x_, y_ = prepare_xy(_x, _y)
                xmin = xmin2xmin(get_xmin(field_name, MAXES), x_, y_, _x, _y)
                x, y = chop_xy(x_, y_, xmin, 'None')
                zs.append(cost_function((tau, beta, yo), x, y))
        res[field_name] = (xs, ys, zs)        
    return res

def urr_vs_urr(fields=GOOD_FITS, fit_style='stretched exponential',
    xmin='custom'):
    (fit_parms, oil_fields) = get_fit_parms(fields=fields, fit_style=fit_style,
        xmin=xmin)
    extrap = extend_productions(fields=fields, fit_style=fit_style, xmin=xmin,
        freq='M')
    our_urrs = extrap.sum()
    our_urrs.name = 'ours'
    their_urrs = dict((k, URRS[k]) for k in GOOD_FITS)
    their_urrs = 1e6 * M3_TO_BARRELS * Series(their_urrs, name='theirs')

    return concat((our_urrs, their_urrs), axis=1)
    
def rate_of_discoveries(bins=[1e4, 1e6, 1e7, 1e8], fields='all'):
    """Plots the number of fields discovered up to time t. This informs us about
    the underlying discovery mechanism. This mechanism can depend on size.
    """
    oil_fields = get_oil_fields()
    if fields == 'all':
        urrs = Series(URRS)[oil_fields.columns].dropna() * 1e6 * M3_TO_BARRELS
    binned_urrs = [urrs[(urrs > bins[i]) & (urrs < bins[i+1])] 
                      for i in range(len(bins)-1)]
    res = []
    plt.ion()
    fig = plt.figure(figsize=(28, 10))
    for i, bin in enumerate(binned_urrs):
        starts = []
        for field in bin.index:
            starts.append(oil_fields[field].dropna().index[0])
        starts = array(starts)
        dates = date_range(START, END)
        number_of_discoveries = [(starts <= date).sum() for date in dates]
        res.append((dates, number_of_discoveries))
        
        fig.add_subplot(1, len(bins)-1, i+1)
        ax = plt.gca()
        ax.plot(dates, number_of_discoveries, 'ok', markersize=4.)
        plt.xlabel('Date of discovery')
        plt.ylabel('Number of fields discovered')
        plt.title('bin=%s-%s' % (log10(bins[i]), log10(bins[i+1])))
       
    return res

def correct_fit_parms(urrs, fit_parms, tolerance=1.5, 
                      conv=1.1):
    """If the urr we get from our extrapolation is bigger or smaller than the
    official urr by the tolerance factor, we change the beta of the fit_parms
    until the newly computed urr falls within some limits set by convergence.
    """
    #hack
    fit_parms, oil_fields = fit_parms
    #Doesn't work. Maybe bug: it thinks that the key is a list (not allowed)
    #however, only my values are list (allowed)
    #fit_parms = {(k, list(v)) for k, v in fit_parms.items()}
    fps = {}
    for k, v in fit_parms.items():
        fps[k] = list(v)
    fit_parms = fps
    ours = urrs['ours']
    theirs = urrs['theirs']

    black_sheep = urrs[(ours/theirs >= tolerance) |
                       (ours/theirs <= 1./tolerance)].index
    step = dict(zip(black_sheep, [1.1]*len(black_sheep)))
    for sheep in black_sheep:
        factor_before = 1. if ours[sheep] > theirs[sheep] else -1.
        while True:
            if factor_before == 1:
                fit_parms[sheep][1] *= step[sheep]
            else:
                fit_parms[sheep][1] /= step[sheep]
            new_urr = extend_production(oil_fields[sheep], 
                          fit_parms[sheep]).sum()
            print ' sheep: %s \n beta: %s\n new urr: %s\n target: %s\n\n' %\
                (sheep, fit_parms[sheep][1], new_urr, new_urr/theirs[sheep])
            if (new_urr < theirs[sheep] * conv) and\
               (new_urr > theirs[sheep] / conv):
                break
            factor_after = 1. if new_urr >= theirs[sheep] else -1.
            if factor_after == factor_before:
                continue
            else:
                step[sheep] = (step[sheep] - 1.) * 0.5 + 1.
                print 'step: %s' % step[sheep]
            factor_before = factor_after
    fit_parms = dict((k, tuple(v)) for k, v in fit_parms.items())

    return (fit_parms, oil_fields)


def extend_bad_fields(oil_fields, fields=BAD_FITS):
    """Some fields do not exhibit a decay that we can model with a stretched
    exponential. It is hard to make any kind of extrapolation. However, we've 
    seen that we can trust the official URR estimation. As such, we will model
    the decay of these "bad" fields by an exponential (beta=1) with tau such
    that the cumulative production equals the official URR up to conv.
    """
    BAD_URRS = Series(URRS)[BAD_FITS] * M3_TO_BARRELS * 1e6
    future_prods = []
    for field in BAD_FITS:
        prod_until_now = oil_fields[field].sum()
        remaining_prod = BAD_URRS[field] - prod_until_now
        last_prod = oil_fields[field].dropna().values[-5:].mean()
        time_until_end = remaining_prod / last_prod

        start = oil_fields[field].index[-1] + MonthBegin()
        end = start + time_until_end * MonthBegin()
        future = date_range(start, end, freq='MS')

        future_prods.append(Series(last_prod, index=future, name=field))
    future_prods = concat(future_prods, axis=1)
    return concat((oil_fields[BAD_FITS], future_prods))

        
def thinning((r, k, p0), t):
    r *= 30    #day -> month
    now = 501 #len(oil_fields)
    p_now = k*p0*exp(r*now) / (k + p0*(exp(r*now))-1)
    #Not very nice conceptually but I know that for all field types, the 
    #discovery rate is decreasing. As such lamda_max = lamda(today)
    lamda_max = r*p_now * (1 - p_now/k)
    dt = -log(rand(1)) / lamda_max
    try:
        t_next = (t + dt * MonthBegin())[0]
    except:
        return (Timestamp('01-02-2260'), False)
    _t_next = len(date_range(START, t_next, freq='MS')) 
    
    p_next = k*p0*exp(r*_t_next) / (k + p0*(exp(r*_t_next))-1)
    lamda_next = r*p_next * (1 - p_next/k)
    accepted = (lamda_max * rand(1) < lamda_next)[0]
    return (t_next, accepted)

def future_oil_production(all_extended_fields, ((rs, ks, ps), (rm, km, pm), 
    (rb, kb, pb))):
    """Simulates future oil production by extending the oil production of each
    field into the future and simulating the discovery of new fields
    """
    fields = {
    'small': all_extended_fields.sum()[log10(all_extended_fields.sum()) < 6.0],
    'medium': all_extended_fields.sum()[(log10(all_extended_fields.sum()) >= 
                  6.0) & (log10(all_extended_fields.sum()) < 7.0)],
    'big': all_extended_fields.sum()[log10(all_extended_fields.sum()) >= 7.0]
        }

    today = Timestamp('02-01-2013')
    t = today
    scenario = all_extended_fields.copy()
    #return scenario
    rkp = {'small': (rs, ks, ps), 'medium': (rm, km, pm), 'big': (rb, kb, pb)}
    for field_size in ('small', 'medium', 'big'):
        t = today
        i = 1
        while t < Timestamp('01-01-2260'):
            t_next, accepted = thinning(rkp[field_size], t)
            t = t_next
            if t >= Timestamp('01-01-2260'):
                t = today
                break
            if accepted:
                picked = choice(fields[field_size].index)[0]
                start = all_extended_fields[picked].dropna().index[0]
                end = all_extended_fields[picked].dropna().index[-1]
                dt = list(all_extended_fields.index).index(t) -\
                    list(all_extended_fields.index).index(start)
                if (Timestamp('01-01-2260') - end).days >= dt * 30:
                    df = DataFrame(all_extended_fields[picked].dropna().\
                         shift(dt, freq='MS'), 
                         columns=['%s_%s' % (field_size, i)])
                    scenario = concat((scenario, df), axis=1)
                    _df = DataFrame(all_extended_fields[picked].dropna(),
                              columns=['%s__%s' % (field_size, i)])
                else:
                    cutoff_id = dt * 30 - (Timestamp('01-01-2260') - end).days
                    cutoff_id = ceil(cutoff_id / 30.)           
                    scenario = concat((scenario, 
                       DataFrame(all_extended_fields[picked][:-cutoff_id].dropna().shift(dt, freq='MS'), columns=['%s_%s' % (field_size, i)])), axis=1)
                i += 1 
    return scenario

