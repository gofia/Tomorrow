import copy
from numpy.core.multiarray import array
from numpy.core.numeric import ndarray
import numpy as np
from scipy.optimize.cobyla import fmin_cobyla
from scipy.optimize.optimize import brute


class SizeBins(object):
    bins = []
    sequence = []

    def __init__(self, size_min, size_max, divisions):
        self.bins = []
        step = float(size_max - size_min) / divisions
        for i in range(0, divisions):
            self.bins.append(SizeBin(
                min=size_min + i * step,
                max=size_min + (i + 1) * step,
            ))

    def append(self, size_bin):
        self.bins.append(size_bin)

    def process(self, size_sequence):
        self.sequence = copy.copy(size_sequence)
        # Reset
        for size_bin in self.bins: size_bin.reset()
        # Process
        for size_idx, size in enumerate(size_sequence):
            for bin_idx, size_bin in enumerate(self.bins):
                if size_bin.min < size <= size_bin.max or (bin_idx == 0 and size_bin.min == size):
                    size_bin.append(1)
                    self.sequence[size_idx] = bin_idx
                else:
                    size_bin.append(0)

    def m(self, i, j):
        return self.bins[j].m[i]

    def m_s(self, i):
        return [self.bins[j].m[i] for j in range(0, len(self.bins))]


class SizeBin(object):
    min = 0
    max = 0
    count = 0
    m = [0]

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def append(self, n):
        self.count += n
        self.m.append(self.m[-1] + n)

    def reset(self):
        self.count = 0
        self.m = [0]


def optimize(size_sequence):
    sizes = [size.get('size', 0) for size in size_sequence]
    size_bins = SizeBins(min(sizes), max(sizes), 2)
    size_bins.process(size_sequence)
    return optimize_sizes_cobyla(size_bins)


def optimize_sizes_cobyla(size_bins):
    likelihood_func = likelihood(size_bins)
    initial_guess = array(initial_x(size_bins))
    constraints = get_constraints(size_bins)
    return fmin_cobyla(likelihood_func, initial_guess, constraints, rhobeg=0.1, rhoend=0.01)


def optimize_sizes_brute(size_bins):
    likelihood_func = likelihood(size_bins)
    ranges = (slice(8, 15, 1.0), slice(3, 10, 1.0), slice(0.05, 1.0, 0.05))
    return brute(likelihood_func, ranges, full_output=True, finish=None)


def likelihood(size_bins):
    def func(x):
        l = len(size_bins.bins)

        if len(x) != 2 * l - 1:
            raise Exception("Wrong number of arguments")

        vec_n = list(x[0:l])
        vec_s = list(x[l:])
        vec_s = vec_s + [1]

        L = -1.0

        for idx, size in enumerate(size_bins.sequence):
            L *= vec_n[size] - size_bins.m(idx, size)
            L *= vec_s[size]
            L /= np.dot(subtract(vec_n, size_bins.m_s(idx)), vec_s)

        return L

    return func


def initial_x(size_bins):
    vec_n = []
    vec_s = []
    for idx, size_bin in enumerate(size_bins.bins):
        vec_n.append(size_bin.count * 2 * (idx + 2) / (idx + 1))
        vec_s.append(idx + 1)
    return vec_n + vec_s[1:]


def get_constraints(size_bins):
    return size_constraints(size_bins) + probability_constraints(size_bins)


def probability_constraints(size_bins):
    constraints = []
    for idx, size_bin in enumerate(size_bins.bins[0:-1]):
        constraints.append(probability_constraint(len(size_bins.bins) + idx))
    return constraints


def probability_constraint(idx):
    def func(x):
        return x[idx]

    return func


def size_constraints(size_bins):
    constraints = []
    for idx, size_bin in enumerate(size_bins.bins):
        constraints.append(size_constraint(idx, size_bin.count))
    return constraints


def size_constraint(idx, size):
    def func(x):
        return x[idx] - size

    return func


def subtract(A, B):
    return [a - b for a, b in zip(A, B)]