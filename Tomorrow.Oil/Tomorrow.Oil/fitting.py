from datetime import datetime

from numpy import array
from numpy import ndarray
from numpy import exp
from numpy import log
from numpy import inf
from numpy import sign

from scipy.optimize import fmin
from scipy.stats import linregress

import matplotlib.pyplot as plt

from pandas import DataFrame
from pandas import Series
from pandas import Timestamp

def fit_exponential(_x, _y=None, xmin=None, xmax=None, show=False, 
    xscale='linear', yscale='linear', ax='None'):
    """Fits an exponential y0 exp(-x / tau) to the data for each x > xmin.
    xmin defines the point from which the exponential regime holds."""

    x_, y_ = prepare_xy(_x, _y)
    xmin = xmin2xmin(xmin, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, xmin, xmax)

    logy = log(y)
    lamda, logy0, _, _, _ = linregress(x, logy)
    tau, y0 = 1. / lamda, exp(logy0)

    if show:
        show_fit('exponential', x_=x_, y_=y_, x=x, y=y, y0=y0, tau=tau,
            xscale=xscale, yscale=yscale, ax=ax)

    return (tau, y0)

def fit_power_law(_x, _y=None, xmin=None, xmax=None, show=False, 
    xscale='linear', yscale='linear', ax='None'):
    """Fits a power law A x ^ -alpha for each x > xmin. xmin defines the point
    from which the power law regime holds."""

    x_, y_ = prepare_xy(_x, _y)
    xmin = xmin2xmin(xmin, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, xmin, xmax)

    logx, logy = log(x), log(y)
    alpha, logy0, _, _, _ = linregress(logx[1:], logy[1:])
    y0 = exp(logy0)

    if show:
        show_fit('power-law', x_=x_, y_=y_, x=x, y=y, y0=y0, alpha=alpha,
            xscale=xscale, yscale=yscale, ax=ax)

    return (alpha, y0)

def fit_stretched_exponential(_x, _y=None, xmin=None, xmax=None, 
    show=False, xscale='linear', yscale='linear', ax='None'):
    """Fits a stretched exponential y0 -exp([x / tau]^beta) for each x > xmin.
    """
 
    x_, y_ = prepare_xy(_x, _y)
    xmin = xmin2xmin(xmin, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, xmin, xmax)

    logy = log(y)
    lamda, logy0, _, _, _ = linregress(x, logy)
    tau, beta, y0 = 1. / lamda, 0.7, exp(logy0)
    tau, beta, y0 = fmin(cost_function, (tau, beta, y0), args=(x, y),
        disp=0)
    
    if show:
        show_fit('stretched exponential', x_=x_, y_=y_, x=x, y=y, y0=y0,
            tau=tau, beta=beta, xscale=xscale, yscale=yscale, ax=ax)
 
    return (tau, beta, y0)   

def cost_function((tau, beta, y0), x, y):
    """Stretched exponential cost function. This is the function to minimize"""
    fit = y0 * exp(sign(tau) * (x/abs(tau))**beta)
    return sum((fit - y)**2 / fit)
    
def prepare_xy(_x, _y=None):
    """Takes in any kind of 2 dimensional data and returns ordinals of x if
    x is a datetime-style object, and y.
    """

    if _y == None:
        if isinstance(_x, Series) or isinstance(_x, DataFrame):
            _x = _x.dropna()
            y = _x.values.flatten()
            _x = _x.index
        elif isinstance(_x, list) or isinstance(_x, ndarray):
            assert len(x) == 2
            y = array(_x[1])
            _x = _x[0]
    else:
        y = _y

    if isinstance(_x[0], datetime):
        x = array([d.toordinal() - _x[0].toordinal() for d in _x])
    else:
        x = array(_x)

    return (x, y)

def chop_xy(x, y, xmin, xmax):
    """Returns the indices of xmin corresponding to the position of xmin in the 
    iterable.
    """
    
    ixmin = x.searchsorted(xmin)
    ixmax = x.searchsorted(xmax)
    ixmax = ixmax if ixmax != 0 else None

    return (x[ixmin:ixmax], y[ixmin:ixmax])

def show_fit(fitstyle, **kwargs):
    """Plots the fit together with the data."""

    plt.ion()
    #fig = plt.figure()
    if kwargs['ax'] == 'None':
        ax = fig.gca()
    else:
        ax = kwargs['ax']
    ax.plot(kwargs['x_'], kwargs['y_'], 'ob')
    if fitstyle == 'power-law':
        ax.plot(kwargs['x'], kwargs['y0'] * kwargs['x'] ** kwargs['alpha'], 
            '-r')
    elif fitstyle == 'exponential':
        ax.plot(kwargs['x'], kwargs['y0'] * exp(kwargs['x'] / kwargs['tau']), 
            '-k')
    elif fitstyle == 'stretched exponential':
        ax.plot(kwargs['x'], kwargs['y0'] * exp(sign(kwargs['tau']) * 
            (kwargs['x'] / abs(kwargs['tau'])) ** kwargs['beta']), '-g')

    ax.set_xscale(kwargs['xscale'])
    ax.set_yscale(kwargs['yscale'])
    plt.draw()

def xmin2xmin(xmin, x_, y_, _x, _y=None):
    """converts the xmin condition to its numerical x coordinate. Ex: xmin='max'
    will be converted to 17, if y_ is at its maximum on day 17
    """
    if xmin == 'max':
        ixmin = list(y_).index(max(y_))
    elif isinstance(xmin, datetime) or isinstance(xmin, str):
        if isinstance(_x, Series) or isinstance(_x, DataFrame):        
            #pandas slicing is inclusive (if xmin is in the index)
            if Timestamp(xmin) in _x.dropna().index:
                ixmin = len(_x[:Timestamp(xmin)].dropna()) - 1
            else:
                ixmin = len(_x[:Timestamp(xmin)].dropna()) 
        elif isinstance(_x, ndarray) or isinstance(_x, list):
            #It is a 2d array or list
            if _y is None:
                _x = _x[0]
            ixmin = list(_x).index(Timestamp(xmin))
    elif xmin == None:
        ixmin = 0
    else:
        if _y is None:
            _x = _x[0]
        ixmin = list(_x).index(xmin) 

    return x_[ixmin]
     
