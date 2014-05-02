from mx.DateTime.DateTime import Timestamp
from numpy import array, exp, arange, where
from datetime import datetime
from scipy.stats import t
from scipy.optimize import fmin
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#This code is based on Peter Cauwel's matlab code.
#Recommended article to read (explaining part of the methodology:
#Quis pendit ipsa pretia: facebook valuation and diagnostic of a bubble based
#on nonlinear demographic dynamics. Peter Cauwels, Didier Sornette (2011).
#link: http://arxiv.org/pdf/1110.1319v2.pdf
#from erpy.ipshell import ipshell


def fit_logistic(dates, values, start_date, confid=None, show_plot=False, 
        xlabel='x', ylabel='y', init_conds=(2., 5.)):
    """Fits logistic function to data and returns r, k and p. 
    Required arguments are the dates and values as well as the starting date.
    confid, the confidence interval can be specified as well."""

    dates = array([float(d.toordinal()) for d in dates])
    values = array([float(v) for v in values])
    start_date = start_date.toordinal()
    dates = dates - start_date

    valmax = values.max()
    idxmax = where(values==values.max())[0][0]
    values /= valmax

    #It can be shown that there is a linear dependence between the population
    #and the growth rate.
    r, k, p = 1. / dates[idxmax], 1., values[0]

    if p == 0:
        p = 0.01 
    #Sometimes the initial estimates of r, k, p are too far from the real values
    #for the optimizer to converge. We therefore, chose other starting points.
    #p0 is usually the problematic parameter.
    mult, len_grid = init_conds
    grid = mult ** arange(-len_grid, len_grid+1)
    ps = p * grid
    rs = r * grid
    ks = k * grid    

    rkp_f = []
    for k in ks:
        for r in rs:
            for p in ps:
                #Here we optimize (r, k, p) without constraint.
                if confid == None:
                    (r, k, p) = fmin(cost_function, (r, k, p), args=(dates, values),
                                          disp=0)
                    #storing the fit_parms and the value of the cost function
                    rkp_f.append(((r, k, p), cost_function((r, k, p), dates, values)))

                #We apply the confidence interval on k, the carrying capacity. 
                #See paper.
                #We then optimize (r, p) with k constant.
                else:
                    tconfid = t.ppf(confid, len(values)-2)
                    k = kconfid = -b / (a + tconfid * std)
                    (r, p) = fmin(cost_function_const, (r, p), args=(dates, values, 
                                                                     kconfid), disp=0, maxiter=10000)
                    rkp_f.append(((r, k, p), cost_function_const((r, p), dates, values, 
                                                              kconfid)))
        #chosing the fit parameters with the smallest cost function
        #for i, _rkp_f in enumerate(rkp_f):
        #    print '%s: %s' % (i, _rkp_f)

    rkp_f = array(sorted([(_r, valmax*_k, valmax*_p) for ((_r, _k, _p),_) in rkp_f], key=lambda x: x[1]))
    rkp_f = [_rkp_f for _rkp_f in rkp_f if (_rkp_f[0] > 0) and (_rkp_f[1] > 0) and\
                (_rkp_f[1] < 1000 * valmax) and (_rkp_f[2] > 0)]
    return rkp_f
    try:
        r, k, p = rkp_f[0]
    except:
        return (0., 0., 0.)
    values *= valmax
    
    fname = 'test.pkl'
    f = open(fname, 'w')
    from pickle import dump
    dump(rkp_f, f)
    f.close()

    if show_plot:
        show_logistic_fit(dates, values, (r, k, p), start_date, xlabel, ylabel)
      
    return r, k, p


def fit_d_logistic(dates, values, start_date, init_conditions=(2., 5.), **kwargs):
    """Fits the time-derivative of the logistic function (the bell shape).
    """
    dates = array([float(d.toordinal()) for d in dates])
    values = array([float(v) for v in values])
    start_date = start_date.toordinal()
    dates = dates - start_date

    cum = array([values[:i].sum() for i in range(len(values))])

    if 'rkp' in kwargs.keys():
        r, k, p = kwargs['rkp']
    else: 
        k = cum[-1]
        r = (4*values.max() / k)**0.5
        p = cum[1]

    multiplier, len_grid = init_conditions
    grid = multiplier ** arange(-len_grid, len_grid+1)
    ps = p * grid
    rs = r * grid
    ks = k * grid    

    print ps
    print rs
    print ks

    rkp_f = []
    for k in ks:
        for r in rs:
            for p in ps:
                (_r, _k, _p) = fmin(cost_function_d_logistic, (r, k, p), args=(dates, values), disp=0)
                rkp_f.append(((_r, _k, _p), cost_function_d_logistic((_r, _k, _p), dates, values)))

    print len(rkp_f)
    rkp_f = array(sorted([(_r, _k, _p) for ((_r, _k, _p), _) in rkp_f], key=lambda x: x[1]))
    #rkp_f = [_rkp_f for _rkp_f in rkp_f if (_rkp_f[0] > 0) and (_rkp_f[1] > 0) and\
    #            (_rkp_f[1] < 1000 * cum[-1]) and (_rkp_f[2] > 0)]
    try:
        r, k, p = rkp_f[0]
    except IndexError:
        return 0., 0., 0.
    
    # f_name = 'test.pkl'
    # f = open(f_name, 'w')
    # from pickle import dump
    # dump(rkp_f, f)
    # f.close()

    return r, k, p


def fit_double_cyclic(dates, values, init_guesses=2, **kwargs):

    print 'Hello'
    #dates = array([float(d.toordinal()) for d in dates])
    _dates = range(len(dates))
    values = array([float(v) for v in values])
    #start_date = start_date.toordinal()
    #dates = dates - start_date
    
    qmax1 = values.max() if 'qmax1' not in kwargs.keys() else kwargs['qmax1']
    qmax2 = values.max() if 'qmax2' not in kwargs.keys() else kwargs['qmax2']
    
    tmax1 = int(0.3 * _dates[-1]) if 'tmax1' not in kwargs.keys() else\
                      _dates[list(dates).index(Timestamp(kwargs['tmax1']))]
    tmax2 = int(0.6 * _dates[-1]) if 'tmax2' not in kwargs.keys() else\
                  _dates[list(dates).index(Timestamp(kwargs['tmax2']))]

    a1 = 0.5 if 'a1' not in kwargs.keys() else kwargs['a1']
    a2 = 0.5 if 'a2' not in kwargs.keys() else kwargs['a2']
     
    print qmax1, qmax2, tmax1, tmax2, a1, a2
    import numpy.random as rd
    import numpy as np 

    qmax1s = qmax1 * 2 * rd.rand(init_guesses)
    qmax2s = qmax2 * 2 * rd.rand(init_guesses)

    tmax1s = tmax1 + np.floor(min(tmax1, _dates[-1]-tmax1) * 
                              (rd.rand(init_guesses) - 0.5))
    tmax2s = tmax2 + np.floor(min(tmax2, _dates[-1]-tmax2) * 
                              (rd.rand(init_guesses) - 0.5))

    a1s = a1 + rd.rand(init_guesses)
    a2s = a2 + rd.rand(init_guesses)

    output = []
    i = 0
    print 'Total = %s' % (init_guesses**6)
    for qmax1 in qmax1s:
        for qmax2 in qmax2s:
            for tmax1 in tmax1s:
                for tmax2 in tmax2s:
                    for a1 in a1s:
                        for a2 in a2s:
                            res =\
                            fmin(cost_cyclic, (qmax1, qmax2, tmax1, tmax2, a1, a2),
                                 args=(_dates, values), maxiter=100000, disp=0)
                            resid = cost_cyclic(res, _dates, values)
                            output.append((res, resid))
                            i += 1
                            if i%100 == 0:
                                print i
    output = array(sorted([_res for (_res,_) in output], key=lambda x: x[1]))    
    return output


def fit_logistic_k_r(p, x, y):
    k, r = 2.5, 3.5
    results = fmin(
        cost_function_k_r,
        (k, r),
        args=(p, x, y),
        maxiter=100000,
        disp=0
    )
    residual = cost_function_k_r((r, k), p, x, y)
    return results[0], results[1], residual


def get_logistic(r, k, p):
    def func(x):
        return k * p * exp(r * x) / (k + p * (exp(r * x) - 1))

    return func


def get_d_logistic(r, k, p):
    logistic = get_logistic(r, k, p)

    def func(x):
        logistic_value = logistic(x)
        return r * logistic_value * (1 - logistic_value / k)

    return func


def cost_cyclic((qmax1, qmax2, tmax1, tmax2, a1, a2), x, y):
    fit = (4 * qmax1 * (exp(-a1*(x-tmax1))) / (1+exp(-a1*(x-tmax1)))**2) +\
          (4 * qmax2 * (exp(-a2*(x-tmax2))) / (1+exp(-a2*(x-tmax2)))**2)
    res = (y - fit)**2 / abs(fit)
    return sum(res)


def cost_function((r, k, p), x, y):
    fit = get_logistic(r, k, p)(x)
    res = (y - fit)**2 / abs(fit)
    return sum(res)


def cost_function_k_r((k, r), p, x, y):
    fit = get_logistic(r, k, p)(x)
    res = (y - fit)**2 / abs(fit)
    return sum(res)


def cost_function_const((r, p), x, y, khe):
    fit = get_logistic(r, khe, p)(x)
    res = (y - fit)**2 / abs(fit)
    return sum(res)


def cost_function_d_logistic((r, k, p), x, y):
    fit = get_d_logistic(r, k, p)(x)
    res = (y-fit)**2 / abs(fit)
    return sum(res)


def compute_logistic(dates, (r, k, p), start_date):
    x = array([float(d.toordinal()) for d in dates])
    start_date = start_date.toordinal()
    x = x - start_date
    return get_logistic(r, k, p)(x)


def show_logistic_fit(x, y, (r, k, p), start_date, x_label, y_label):
    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(111)
    x_fit = arange(2*x[-1])
    y_fit = k * p * exp(r * x_fit) / (k + p * (exp(r * x_fit) -1))
    x = [datetime.fromordinal(int(d)) for d in x+start_date]
    x_fit = [datetime.fromordinal(int(d)) for d in x_fit+start_date]
    ax.plot(x, y, 'ok')
    ax.plot(x_fit, y_fit, '-k')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(x_fit[0], x_fit[-1])
    t_format = DateFormatter("%b-%y")
    ax.xaxis.set_major_formatter(t_format)
    plt.show()

