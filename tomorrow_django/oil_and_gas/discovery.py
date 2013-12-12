from cmath import log
import copy
import random
from numpy.core.multiarray import array
import numpy as np
from scipy.optimize.cobyla import fmin_cobyla
from scipy.optimize.optimize import brute
from oil_and_gas.fitting import fit_exponential
from oil_and_gas.utils import traverse, list_get, add_months


class DiscoveryGenerator:
    fields = []
    sizes = []
    size_bins = None
    scenarios = []
    pdf = []

    def __init__(self, fields):
        self.fields = fields
        self.sizes = [field.extrapolated_total_production_oil for field in fields]
        self.size_bins = SizeBins(min(self.sizes), max(self.sizes), 2)
        self.size_bins.process(self.sizes)
        self.size_bins.init_date_sequences(self.fields)
        self.init_scenarios()

    def init_scenarios(self):
        result = optimize_sizes_brute(self.size_bins)

        for i in traverse(result[3]):
            scenario = copy.deepcopy(i)
            scenario[1] = list_get(result[2], i[1]) + [1]
            self.scenarios.append(scenario)

        self.scenarios.sort(key=lambda item: item[0])

        probability = 0
        for scenario in self.scenarios:
            self.pdf.append(probability)
            probability += scenario[0]

        self.pdf = self.pdf / self.pdf[-1]

    def random_scenario(self):
        r = random.random()
        scenario_idx = next(p for p in self.pdf if p > r)
        return self.scenarios[scenario_idx]

    def process_scenario(self, scenario):
        scenario = self.random_scenario()



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
                if size_bin.try_append(size, bin_idx):
                    self.sequence[size_idx] = bin_idx

    def m(self, i, j):
        return self.bins[j].m[i]

    def m_s(self, i):
        return [self.bins[j].m[i] for j in range(0, len(self.bins))]

    def get_ranges(self):
        ranges = ()
        probability_ranges = ()
        for size_bin in self.bins:
            ranges += (slice(size_bin.count + 1, size_bin.count * 2, 1.0),)
            probability_ranges += (slice(0.05, 1.0, 0.05),)
        ranges += probability_ranges[:-1]
        return ranges

    def init_date_sequences(self, fields):
        for field in fields:
            for bin in self.bins:
                bin.try_add_date_sequence(field)


class SizeBin(object):
    min = 0
    max = 0
    count = 0
    m = [0]
    sizes = []
    tau = -1
    y0 = 1
    initialized = False
    date_sequence = []

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def append(self, n):
        self.initialized = False
        self.count += n
        self.m.append(self.m[-1] + n)

    def reset(self):
        self.initialized = False
        self.count = 0
        self.m = [0]

    def try_append(self, size, bin_idx):
        if self.min < size <= self.max or (bin_idx == 0 and self.min == size):
            self.append(1)
            self.sizes.append(size)
            return True
        else:
            self.append(0)
            return False

    def init_generator(self):
        if self.initialized:
            return

        self.initialized = True
        total = self.sizes.count()
        pdf = []
        for i in range(0.0, 100.0):
            max_size = self.min + (self.max - self.min) * i / 100
            count = [1 for size in self.sizes if size >= max_size]
            pdf.append(count/total)

        self.tau, self.y0 = fit_exponential(pdf)

    def generate_size(self):
        self.init_generator()
        r = random.random()
        size = self.min + (log(r / self.y0) / self.tau) * (self.max - self.min) / 100
        return size

    def try_add_date_sequence(self, field):
        if self.contains(field):
            self.date_sequence.append(field.discovery)

    def contains(self, field):
        return self.min <= field.extrapolated_total_production_oil <= self.max

    def cumulative_discoveries(self):
        data = [0]
        self.date_sequence.sort()
        date = self.date_sequence[0]
        counter = 0
        while counter < len(self.date_sequence):
            if date == self.date_sequence[counter]:
                counter += 1
                data.append(counter)
            else:
                data.append(data[-1])
            date = add_months(date, 1)
        return data

    def compute_logistic(self, N):
        x = range(0, len(self.date_sequence))
        pass


def optimize(sizes):
    size_bins = SizeBins(min(sizes), max(sizes), 2)
    size_bins.process(sizes)
    return optimize_sizes_brute(size_bins)


def optimize_sizes_cobyla(size_bins):
    likelihood_func = likelihood(size_bins)
    initial_guess = array(initial_x(size_bins))
    constraints = get_constraints(size_bins)
    return fmin_cobyla(likelihood_func, initial_guess, constraints, rhobeg=0.1, rhoend=0.01)


def optimize_sizes_brute(size_bins):
    likelihood_func = likelihood(size_bins)
    ranges = size_bins.get_ranges()
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