from datetime import datetime
from mx.DateTime.DateTime import Timestamp

from numpy import array, ndarray, exp, log, sign, mean

from scipy.optimize import fmin
from scipy.stats import linregress

import matplotlib.pyplot as plt

from pandas import DataFrame, Series

from .fit_logistic import cost_function as cost_function_logistic


def chop_xy(x, y, x_min, x_max):
    """Returns the indices of x_min corresponding to the
    position of x_min in the iterable.
    """
    x_min_found = x.searchsorted(x_min)
    x_max_found = x.searchsorted(x_max)
    x_max_found = x_max_found if x_max_found != 0 else None
    return x[x_min_found:x_max_found], y[x_min_found:x_max_found]


def prepare_xy(_x, _y=None):
    """Takes in any kind of 2 dimensional data and returns ordinals of x if
    x is a datetime-style object, and y.
    """

    y = _y
    if _y is None:
        if isinstance(_x, Series) or isinstance(_x, DataFrame):
            _x = _x.dropna()
            y = _x.values.flatten()
            _x = _x.index
        elif isinstance(_x, list) or isinstance(_x, ndarray):
            assert len(_x) == 2
            y = array(_x[1])
            _x = _x[0]

    if isinstance(_x[0], datetime):
        x = array([d.toordinal() - _x[0].toordinal() for d in _x])
    else:
        x = array(_x)

    return x, y


def x_min_2_x_min(x_min, x_, y_, _x, _y=None):
    """Converts the x_min condition to its numerical x coordinate. Ex: x_min='max'
    will be converted to 17, if y_ is at its maximum on day 17.
    """

    i_x_min = 0
    if x_min == 'max':
        i_x_min = list(y_).index(max(y_))
    elif isinstance(x_min, datetime) or isinstance(x_min, str):
        if isinstance(_x, Series) or isinstance(_x, DataFrame):
            #pandas slicing is inclusive (if x_min is in the index)
            if Timestamp(x_min) in _x.dropna().index:
                i_x_min = len(_x[:Timestamp(x_min)].dropna()) - 1
            else:
                i_x_min = len(_x[:Timestamp(x_min)].dropna())
        elif isinstance(_x, ndarray) or isinstance(_x, list):
            #It is a 2d array or list
            if _y is None:
                _x = _x[0]
            i_x_min = list(_x).index(Timestamp(x_min))
    elif x_min is None:
        i_x_min = 0
    else:
        if _y is None:
            _x = _x[0]
        i_x_min = list(_x).index(x_min)

    return x_[i_x_min]


def remove_zeros(xs, ys):
    x_no_zeros = []
    y_no_zeros = []
    for i in range(len(ys)):
        if ys[i] != 0:
            x_no_zeros.append(xs[i])
            y_no_zeros.append(ys[i])
    return x_no_zeros, y_no_zeros


def fit_exponential(_x, _y=None, x_min=None, x_max=None, show=False,
                    x_scale='linear', y_scale='linear', ax='None', title='None'):
    """Fits an exponential y0 exp(-x / tau) to the data for each x > x_min.
    x_min defines the point from which the exponential regime holds."""

    x_, y_ = prepare_xy(_x, _y)
    x_min = x_min_2_x_min(x_min, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, x_min, x_max)

    x_no_zeros, y_no_zeros = remove_zeros(x, y)
    logy = log(y_no_zeros)
    param_lambda, logy0, _, _, _ = linregress(x_no_zeros, logy)
    tau, y0 = 1. / param_lambda, exp(logy0)

    if show:
        show_fit('exponential', x_=x_, y_=y_, x=x, y=y, y0=y0, tau=tau,
                 x_scale=x_scale, y_scale=y_scale, ax=ax, title=title)

    return tau, y0


def fit_power_law(_x, _y=None, x_min=None, x_max=None, show=False,
                  x_scale='linear', y_scale='linear', ax='None', title='None'):
    """Fits a power law A x ^ -alpha for each x > x_min. x_min defines the point
    from which the power law regime holds."""

    x_, y_ = prepare_xy(_x, _y)
    x_min = x_min_2_x_min(x_min, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, x_min, x_max)

    x_no_zeros, y_no_zeros = remove_zeros(x, y)
    log_x, log_y = log(x_no_zeros), log(y_no_zeros)
    alpha, logy0, _, _, _ = linregress(log_x[1:], log_y[1:])
    y0 = exp(logy0)

    if show:
        show_fit('power-law', x_=x_, y_=y_, x=x, y=y, y0=y0, alpha=alpha,
                 x_scale=x_scale, y_scale=y_scale, ax=ax, title=title)

    return alpha, y0


def fit_stretched_exponential(_x, _y=None, x_min=None, x_max=None,
                              x_min_guess=None, y0=None, tau=None, beta=None,
                              show=False, x_scale='linear', y_scale='linear',
                              ax='None', title='None'):
    """Fits a stretched exponential y0 -exp([x / tau]^beta) for each x > x_min.
    """

    x_, y_ = prepare_xy(_x, _y)
    x_min = x_min_2_x_min(x_min, x_, y_, _x, _y)
    x, y = chop_xy(x_, y_, x_min, x_max)

    if x_min != x_min_guess or y0 is None or tau is None or beta is None:
        x_no_zeros, y_no_zeros = remove_zeros(x, y)
        logy = log(y_no_zeros)
        param_lambda, logy0, _, _, _ = linregress(x_no_zeros, logy)
        tau, beta, y0 = 1. / param_lambda, 0.7, exp(logy0)

    tau, beta, y0 = fmin(cost_function, (tau, beta, y0), args=(x, y), disp=0)
    tau, beta, y0 = fmin(cost_function_integral, (tau, beta, y0), args=(x, y), disp=0)
    
    if show:
        show_fit('stretched exponential', x_=x_, y_=y_, x=x, y=y, y0=y0,
                 tau=tau, beta=beta, x_scale=x_scale, y_scale=y_scale, ax=ax,
                 title=title)
 
    return x_min, tau, beta, y0


def get_stretched_exponential(y0, tau, beta):
    def func(x):
        return y0 * exp(sign(tau) * (x / abs(tau)) ** beta)

    return func


def cost_function((tau, beta, y0), x, y):
    """Stretched exponential cost function. This is the function to minimize"""

    fit = get_stretched_exponential(y0, tau, beta)(x)
    return sum((fit - y)**2 / fit)


def cost_function_integral((tau, beta, y0), x, y):
    """Stretched exponential cost function. This is the function to minimize"""

    fit = get_stretched_exponential(y0, tau, beta)(x)
    return sum((fit - y)**2 / fit) + abs(sum(fit - y))


def r_squared(fit, x, y):
    y_average = mean(y)
    ss_total = sum((y - y_average)**2)
    ss_residual = sum((y-fit(x))**2)
    if ss_total == 0:
        return 0
    r_squared = 1 - ss_residual / ss_total
    return r_squared


def fit_logistic(_x, _y, k, r=None):
    """Fits a logistic curve.
    """

    x, y = prepare_xy(_x, _y)

    if r is None:
        r = 1

    cost_func = cost_function_logistic_reduced(k, 1)

    r, p = fmin(cost_func, (r,), args=(x, y), disp=0)

    return r, k, p


def cost_function_logistic_reduced(k, p):
    def func((r,), x, y):
        cost_function_logistic((r, k, p), x, y)

    return func


def show_fit(fit_style, **kwargs):
    """Plots the fit together with the data."""

    plt.ion()

    if kwargs['ax'] == 'None':
        fig = plt.figure()
        ax = fig.gca()
    else:
        ax = kwargs['ax']

    ax.plot(kwargs['x_'], kwargs['y_'], 'ob')

    x = kwargs['x']
    y0 = kwargs['y0']

    if fit_style == 'power-law':
        alpha = kwargs['alpha']
        ax.plot(x, y0 * x ** alpha, '-r')
    elif fit_style == 'exponential':
        tau = kwargs['tau']
        ax.plot(x, y0 * exp(x / tau), '-k')
    elif fit_style == 'stretched exponential':
        tau = kwargs['tau']
        beta = kwargs['beta']
        ax.plot(x, y0 * exp(sign(tau) * (x / abs(tau)) ** beta), '-g')

    ax.set_xscale(kwargs['x_scale'])
    ax.set_yscale(kwargs['y_scale'])
    ax.set_title(kwargs['title'])
    plt.draw()
    # TODO later
    # plt.savefig("C:/Users/lucas.fievet/PycharmProjects/Tomorrow/tomorrow_django/oil_and_gas/figure.png")
