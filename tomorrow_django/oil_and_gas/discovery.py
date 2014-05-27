#
# Project: Tomorrow
#
# 07 February 2014
#
# Copyright 2014 by Lucas Fievet
# Salerstrasse 19, 8050 Zuerich
# All rights reserved.
#
# This software is the confidential and proprietary information
# of Lucas Fievet. ("Confidential Information"). You
# shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license
# agreement you entered into with Lucas Fievet.
#

from cmath import log

import copy
import random
import datetime
import json

from numpy.core.multiarray import array
import numpy as np
from scipy.optimize.cobyla import fmin_cobyla
from scipy.optimize.optimize import brute

from .models import Country, Field, DiscoveryScenario, CachedResult
from .processing import FieldProcessor
from .fitting import fit_exponential
from .fit_logistic import fit_logistic_r_p, get_logistic
from .fitting import fit_stretched_exponential, get_stretched_exponential
from .utils import traverse, list_get, add_months, diff_months_abs, make_plot, start_plot


class DiscoveryGenerator:
    date_max = datetime.date(2008, 1, 1)
    fields = []
    sizes = []
    size_bins = None
    scenarios = []
    pdf = []
    _oldest_unstable_field = None
    n_scenarios = 100

    def __init__(self, country):
        self.country = Country.objects.get(name=country)
        print "Generating discoveries for " + country

        self.fields = Field.objects.filter(
            country=country,
            discovery__lt=self.date_max,
        ).order_by('discovery').all()
        print "Found {0} fields.".format(len(self.fields))

        self.sizes = [field.extrapolated_total_production_oil for field in self.fields]
        self.sizes = [size for size in self.sizes if size > 0]
        self.min_size = min(self.sizes)
        self.max_size = max(self.sizes)
        # self.median_size = np.median(self.sizes)
        self.median_size = 40E6  # 40 for UK, 50 for NO
        print "Number sizes: {0}".format(len(self.sizes))
        print "Sizes: {0}".format(self.sizes)
        print "Min size: {0}".format(self.min_size)
        print "Median size: {0}".format(self.median_size)
        print "Max size: {0}".format(self.max_size)

        self.size_bins = SizeBins(self.min_size, self.max_size, self.median_size)

        print "Process sizes"
        self.size_bins.process(self.sizes)

        print "Initialize date sequence"
        self.size_bins.init_date_sequences(self.fields)

        print "Initialize scenarios"
        self.init_scenarios()

        print "Initialize average productions"
        self.average_dwarf_production = self.get_average_production(
            0,
            self.median_size,
        )
        self.average_giant_production = self.get_average_production(
            self.median_size,
            self.max_size,
        )

        print "Initialize size fits"
        self.dwarf_size_fit = self.get_size_fit(0, self.median_size)
        self.giant_size_fit = self.get_size_fit(self.median_size, self.max_size)

        print "Plot logistics"
        self.time_dwarf, self.logistic_dwarf = self.get_logistic(
            0,
            self.median_size
        )
        self.x_dwarf = range(0, len(self.logistic_dwarf))
        # make_plot(self.x_dwarf, self.logistic_dwarf, "Month", "Number dwarf fields")

        self.time_giant, self.logistic_giant = self.get_logistic(
            self.median_size,
            self.max_size
        )
        self.x_giant = range(0, len(self.logistic_giant))
        # make_plot(self.x_giant, self.logistic_giant, "Month", "Number giant fields")

        self.logistic_plot = start_plot(
            "Time",
            "Number of discovered fields",
            "Extrapolating Norwegian Field Discoveries"
        )
        p1 = self.logistic_plot.plot(self.time_dwarf, self.logistic_dwarf, 'bo', label="Dwarf")
        p2 = self.logistic_plot.plot(self.time_giant, self.logistic_giant, 'go', label="Giants")
        self.logistic_plot.legend(("Dwarfs", "Giants"), loc='upper left')

    def init_scenarios(self):
        db_scenarios = DiscoveryScenario.objects.filter(country=self.country)
        # db_scenarios.delete()

        if db_scenarios.count() > 0:
            self.scenarios = db_scenarios.order_by('pdf').all()
            self.pdf = map(lambda x: x.pdf, list(self.scenarios))
            return

        result = optimize_sizes_brute(self.size_bins)

        for i in traverse(result[3]):
            scenario = copy.deepcopy(i)
            scenario = (scenario[0], list_get(result[2], scenario[1]) + [1])
            self.scenarios.append(scenario)

        self.scenarios.sort(key=lambda item: item[0])
        print "Found {0} scenarios.".format(len(self.scenarios))

        probability = 0
        discovery_scenarios = []
        for scenario in self.scenarios:
            probability += abs(scenario[0])
            self.pdf.append(probability)

            # Check if we have enough scenarios
            if abs(scenario[0]) / probability < 0.001:
                break

            # Save to database
            probability_total = scenario[1][2] + scenario[1][3]
            scenario[1][2] = scenario[1][2] / probability_total
            scenario[1][3] = scenario[1][3] / probability_total
            discovery_scenarios.append(DiscoveryScenario.objects.create(
                country=self.country,
                probability=abs(scenario[0]),
                pdf=probability,
                number_dwarfs=scenario[1][0],
                number_giants=scenario[1][1],
                probability_dwarf=scenario[1][2],
                probability_giant=scenario[1][3],
            ))

        print "Kept {0} scenarios with total probability 0.999.".format(
            len(discovery_scenarios)
        )
        for scenario in discovery_scenarios:
            scenario.pdf /= self.pdf[-1]
            scenario.save()

        self.pdf /= self.pdf[-1]
        self.scenarios = discovery_scenarios

    def get_logistic(self, min_size, max_size):
        print "Get logistic"
        fields = []
        for field in self.fields:
            if min_size < field.extrapolated_total_production_oil <= max_size:
                fields.append(field)

        print "Found {0} fields between {1} and {2}.".format(len(fields), min_size, max_size)

        youngest = min(map(lambda x: x.discovery, fields))
        n_months = diff_months_abs(youngest, add_months(self.date_max, 4))
        times = [add_months(copy.copy(youngest), n) for n in range(0, n_months)]
        discoveries = np.zeros(n_months)

        for field in fields:
            n_months = diff_months_abs(youngest, field.discovery)
            field_discovery = np.concatenate(
                (np.zeros(n_months), np.ones(len(discoveries) - n_months))
            )
            discoveries = discoveries + field_discovery

        return times, discoveries

    def get_average_production(self, min_size, max_size):
        print "Get average production"
        cache_name = "average-production-{0}-{1}-{2}".format(self.country.name, min_size, max_size)
        cached_result, created = CachedResult.objects.get_or_create(name=cache_name)
        if not created:
            return np.array(cached_result.data)

        fields = []
        max_length = 0
        for field in self.fields:
            if min_size < field.extrapolated_total_production_oil <= max_size:
                field.oil_productions = FieldProcessor.deserialize_productions(
                    field.production_oil
                )
                max_length = max(max_length, len(field.production_oil))
                fields.append(field)

        print "Found {0} fields between {1} and {2}.".format(len(fields), min_size, max_size)

        productions = []

        for field in fields:
            for idx, production in enumerate(field.oil_productions):
                if len(productions) <= idx:
                    productions.append([])
                if field.extrapolated_total_production_oil < production.object.production_oil:
                    print "{0}, {1}, {2}, {3}".format(
                        field.name,
                        production.object.production_oil,
                        field.extrapolated_total_production_oil,
                        field.total_production_oil,
                    )
                productions[idx].append(
                    production.object.production_oil / field.extrapolated_total_production_oil
                )

        for production in productions:
            cached_result.data.append((np.average(production), np.std(production)))

        cached_result.set_data()
        cached_result.save()

        # make_plot(
        #     np.array(range(0, len(avg_production))),
        #     map(lambda x: x[0], avg_production),
        #     "Month",
        #     "Average production",
        # )
        return cached_result.data

    def get_size_fit(self, min_size, max_size):
        print "Get size fit"
        sizes = []
        for field in self.fields:
            if min_size < field.extrapolated_total_production_oil <= max_size:
                sizes.append(field.extrapolated_total_production_oil)

        print "Found {0} fields between {1} and {2}.".format(len(sizes), min_size, max_size)

        sizes = np.array(sizes)
        bins = np.linspace(min_size, max_size, 50)
        digitized = np.digitize(sizes, bins)
        size_pdf = np.bincount(digitized)[1:]
        size_pdf = np.cumsum(size_pdf)
        size_pdf = [(np.float(s) / np.float(len(sizes))) for s in size_pdf]
        size_pdf = np.ones(len(size_pdf)) - size_pdf
        bins = np.linspace(min_size, max_size, len(size_pdf))

        x_min, tau, beta, y0 = fit_stretched_exponential(
            bins,
            size_pdf,
            y0=1,
            tau=-1.0,
            beta=1.0,
            show=False,
        )

        # make_plot(
        #     bins,
        #     size_pdf,
        #     "Bin",
        #     "Number fields",
        #     bins,
        #     get_stretched_exponential(y0, tau, beta)(bins),
        # )

        return get_stretched_exponential(y0, tau, beta)

    @staticmethod
    def get_random_size(fit, min_size, max_size):
        r = random.random()
        found_size = 0
        # print "{0} / {1}".format(min_size, max_size)
        for size in np.linspace(min_size, max_size, 100):
            # print "fit: {0}".format(fit(size))
            # print "r: {0}".format(r)
            if fit(size) < r:
                found_size = size
                break
        if found_size == 0:
            found_size = max_size
        return found_size

    def oldest_unstable_field(self):
        if self._oldest_unstable_field is not None:
            return self._oldest_unstable_field
        unstable_fields = [field for field in self.fields
                           if not field.stable
                           and field.active
                           and field.current_production_oil > 0]
        discovery_dates = map(lambda x: x.discovery, unstable_fields)
        self._oldest_unstable_field = min(discovery_dates)
        return self._oldest_unstable_field

    def random_scenario(self):
        r = random.random()
        scenario_idx = next(idx for idx, p in enumerate(self.pdf) if p > r)
        print "Selected scenarios {0}.".format(scenario_idx)
        print "Dwarf probability {0}.".format(self.scenarios[scenario_idx].probability_dwarf)
        return self.scenarios[scenario_idx]

    def compute_future_dwarfs(self):
        print "Compute future dwarfs."
        avg, err = None, None
        for i in range(0, self.n_scenarios):
            try:
                scenario = self.random_scenario()
                scenario_avg, scenario_err = self.process_size(
                    scenario.number_dwarfs,
                    self.x_dwarf,
                    self.logistic_dwarf,
                    self.dwarf_size_fit,
                    self.average_dwarf_production,
                    self.time_dwarf,
                    0.0,
                    self.median_size,
                )
                if avg is None:
                    avg, err = scenario_avg, scenario_err
                else:
                    avg += scenario_avg
                    err += scenario_err
            except Exception:
                pass
        avg /= self.n_scenarios
        err /= self.n_scenarios
        # make_plot(
        #     range(0, len(scenario_avg)),
        #     avg,
        #     "Month",
        #     "Discovery production",
        # )

        # start_date = copy.copy(self.oldest_unstable_field())
        # start_date = add_months(start_date, 36)
        start_date = add_months(self.date_max, -40)
        print "Dwarf discovery start date {0}.".format(start_date)
        future = []
        for idx, production in enumerate(avg):
            if production > 0:
                future.append({
                    'date': str(start_date),
                    'average': production,
                    'sigma': err[idx],
                })
                start_date = add_months(start_date, 1)
        self.country.future_dwarfs = json.dumps(future)
        self.country.save()

    def compute_future_giants(self):
        print "Compute future giants."
        avg, err = None, None
        for i in range(0, self.n_scenarios):
            try:
                scenario = self.random_scenario()
                scenario_avg, scenario_err = self.process_size(
                    scenario.number_giants,
                    self.x_giant,
                    self.logistic_giant,
                    self.giant_size_fit,
                    self.average_giant_production,
                    self.time_giant,
                    self.median_size,
                    self.max_size,
                )
                if avg is None:
                    avg, err = scenario_avg, scenario_err
                else:
                    avg += scenario_avg
                    err += scenario_err
            except Exception:
                pass
        avg /= self.n_scenarios
        err /= self.n_scenarios
        # make_plot(
        #     range(0, len(scenario_avg)),
        #     avg,
        #     "Month",
        #     "Discovery production",
        # )

        # start_date = copy.copy(self.oldest_unstable_field())
        # start_date = add_months(start_date, 36)
        start_date = add_months(self.date_max, -40)
        print "Giant discovery start date {0}.".format(start_date)
        future = []
        for idx, production in enumerate(avg):
            if production > 0:
                future.append({
                    'date': str(start_date),
                    'average': production,
                    'sigma': err[idx],
                })
                start_date = add_months(start_date, 1)
        self.country.future_giants = json.dumps(future)
        self.country.save()

    def process_size(self, number, time, logistic, size_fit, avg_production, lol, min_size, max_size):
        print "Scenario has {0} dwarfs.".format(number)
        r_dwarf, p_dwarf, residual_dwarf = fit_logistic_r_p(
            number,
            time,
            logistic,
            0.1,
            1
        )
        last_month = time[-1]
        range_future = range(last_month + 1, last_month + 12 * 30)
        x_future = np.array(time + range_future)
        fit = get_logistic(r_dwarf, number, p_dwarf)(x_future)
        times = [add_months(copy.copy(lol[0]), n) for n in range(0, len(x_future))]
        self.logistic_plot.plot(times, fit)
        # make_plot(
        #     self.x_dwarf,
        #     logistic,
        #     "Month",
        #     "Number fields",
        #     x_future,
        #     fit,
        # )

        future_len = len(x_future) - len(time)
        x_discoveries = range(0, future_len)
        discoveries = (fit - logistic[-1])[len(time):]
        discoveries_max = max(discoveries)
        randoms = [2 * (0.5 - random.random()) for i in range(0, len(discoveries))]
        randoms = np.cumsum(randoms)
        randoms /= max(abs(randoms))
        randoms = [2 * r * (discoveries_max - discoveries[idx]) for idx, r in enumerate(randoms)]
        discoveries = discoveries + randoms
        discoveries = [min(discovery, discoveries_max) for discovery in discoveries]
        production = np.zeros(future_len)
        production_err = np.zeros(future_len)
        next_step = 0
        avg = map(lambda p: p[0], avg_production)
        err = map(lambda p: p[1], avg_production)
        count = 0
        for x in x_discoveries:
            if discoveries[x] > next_step:
                count += 1
                field_size = self.get_random_size(size_fit, min_size, max_size)
                # print field_size
                field_production = np.zeros(len(avg))
                field_production_err = np.zeros(len(err))
                for idx, e in enumerate(avg):
                    field_production[idx] = e * field_size
                for idx, e in enumerate(err):
                    field_production_err[idx] = e * field_size
                field_production = np.array(field_production[0:(future_len - x)])
                field_production_err = np.array(field_production_err[0:(future_len - x)])
                try:
                    for idx, e in enumerate(np.concatenate((np.zeros(x), field_production), axis=0)):
                        production[idx] += e
                    for idx, e in enumerate(np.concatenate((np.zeros(x), field_production_err), axis=0)):
                        production_err[idx] += e
                except:
                    print np.concatenate((np.zeros(x), field_production), axis=0)
                next_step += 1
        print "{0}/{1}".format(count, discoveries_max)

        # make_plot(
        #     x_discoveries,
        #     production,
        #     "Month",
        #     "Discovery production",
        # )
        return production, production_err

class SizeBins(object):
    bins = []
    sequence = []

    def __init__(self, size_min, size_max, median):
        self.bins = []
        self.bins.append(SizeBin(
            bin_min=size_min,
            bin_max=median,
        ))
        self.bins.append(SizeBin(
            bin_min=median,
            bin_max=size_max,
        ))

    def append(self, size_bin):
        self.bins.append(size_bin)

    def process(self, size_sequence):
        self.sequence = copy.copy(size_sequence)
        # Reset
        for size_bin in self.bins:
            size_bin.reset()
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
            if size_bin.count < 100:  # < 150 for UK
                ranges += (slice(size_bin.count + 1, size_bin.count + 10, 1.0),)
                probability_ranges += (slice(0.05, 1.0, 0.05),)
            else:
                ranges += (slice(size_bin.count * 1.0, size_bin.count * 2, 1.0),)  # +1 and * 1.25 for U.K.
                probability_ranges += (slice(0.05, 1.0, 0.05),)
        ranges += probability_ranges[:-1]
        return ranges

    def init_date_sequences(self, fields):
        for field in fields:
            for bin_item in self.bins:
                bin_item.try_add_date_sequence(field)


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

    def __init__(self, bin_min, bin_max):
        self.min = bin_min
        self.max = bin_max

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

    def compute_logistic(self):
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

        likelihood_value = -1.0

        for idx, size in enumerate(size_bins.sequence):
            likelihood_value *= vec_n[size] - size_bins.m(idx, size)
            likelihood_value *= vec_s[size]
            likelihood_value /= np.dot(subtract(vec_n, size_bins.m_s(idx)), vec_s)

        return likelihood_value

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


def subtract(list_a, list_b):
    return [a - b for a, b in zip(list_a, list_b)]
