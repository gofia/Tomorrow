__author__ = 'lucas.fievet'


from numpy.lib.function_base import average
from numpy.core.fromnumeric import std
from numpy.core.umath import log, exp
from scipy.optimize import fmin
from scipy.stats import linregress


class LpplFitting():
    def period_guess(self, y_s, t_0):
        extrema = []
        spacings = [log(extrema[i+1] - t_0) - log(extrema[i] - t_0)
                    for i in range(1, len(extrema))]
        omegas = spacings / 2 * 22 / 7
        omega_guess = average(omegas)
        omega_std = std(omegas)
        return omega_guess, omega_std

    def power_law_guess(self, y_s):
        log_x, log_y = log(range(1, len(y_s))), log(y_s)
        alpha, logy0, _, _, _ = linregress(log_x[1:], log_y[1:])
        y0 = exp(logy0)
        return y0, alpha