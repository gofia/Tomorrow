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

import abc
import copy
import numpy as np
import json

from cmath import sqrt
from numpy import average, std, abs
from numpy.core.numeric import array
from scipy.signal import argrelextrema
from dateutil import relativedelta
from datetime import date

from celery._state import current_task

from django.core import serializers

from .models import (Field, FieldProduction, Country,
                     CountryProduction, StretchedExponential)
from .fitting import get_stretched_exponential
from .utils import add_months, diff_months, diff_months_abs


class ProductionProcessor():
    date_max = date(2015, 1, 1)
    production_type = None
    processed_type = None
    processed = None
    productions = None
    dates = None
    x_s = None
    y_s = None

    def __init__(self):
        pass

    def compute(self, name):
        to_process = self.get_list(name)
        return self.compute_all(to_process)

    @abc.abstractmethod
    def get_list(self, name):
        return

    def compute_all(self, field_list):
        for item in field_list:
            self.compute_item(item)
        return len(field_list)

    def compute_item(self, options):
        print "Load data"
        self.load_data(options)
        if not len(self.productions) == 0:
            print "Set information"
            self.set_information()
            print "Compute fit"
            self.compute_fit()
        print "Save processed"
        self.processed.save()
        self.processed.fits.all().delete()
        self.compute_fits(self.processed, self.productions, options)

    def load_data(self, options):
        name = options.get('name', '')
        self.productions = self.production_type.objects.filter(
            name=name,
            date__lte=self.date_max,
        ).all().order_by('date')
        if len(self.productions) == 0:
            return
        self.processed, created = self.processed_type.objects.get_or_create(name=name)
        self.dates, self.x_s, self.y_s = self.get_plot_data()

    def compute_fits(self, processed, productions, options):
        maximum_date = self.get_maximum()
        self.set_maximum(maximum_date, options)
        dates, x, y = self.get_plot_data(options)
        x_min_guess, y0_guess, tau_guess, beta_guess = None, None, None, None
        i_list, fit_list = [], []
        last_good_fit = None
        fit = None

        for i in range(2, len(x)):
            # If the fit is not zero, reuse the previous values as a first guess
            if fit is not None:
                # print fit.x_min
                x_min_guess, y0_guess, tau_guess, beta_guess = fit.x_min, fit.A, fit.tau, fit.beta

            fit, created = self.get_stretched_exponential(processed, dates[i])
            if fit.compute_fit(x[0:i], y[0:i], x_min_guess, y0_guess, tau_guess, beta_guess):
                try:
                    fit.date_begin = productions[0].date + relativedelta.relativedelta(months=fit.x_min)
                    fit.length = i

                    # Compute error
                    if diff_months_abs(fit.date_end, fit.date_begin) > 12 and len(y[i:]) > 12:
                        fit.sum_error = fit.compute_error(x[i:-1], y[i:-1])

                    if len(i_list) > 0 and fit.x_min != last_good_fit.x_min:
                        i_list, fit_list = [], []

                    fit.save()
                    i_list.append(i)
                    fit_list.append(copy.copy(fit))
                    last_good_fit = copy.copy(fit)
                    print "SUCCESS: " + productions[0].name + " - " + \
                          fit.date_begin.__str__() + " - " + fit.date_end.__str__()
                except Exception as e:
                    print "EXCEPTION: " + e.__str__()
                    fit.delete()
                    fit = None
            else:
                print "FAILURE"
                fit.delete()
                # print "last {0}".format(last_good_fit.x_min)
                fit = last_good_fit

            if hasattr(current_task, 'update_state'):
                pass
                # current_task.update_state(
                #     state='PROGRESS',
                #     meta={'percent': round(100.0 * i / len(x))}
                # )

        avg_tau = None
        tau_list = [fit.tau for fit in fit_list]
        for i in range(2, len(i_list)):
            if i > (len(i_list) / 5.0) and avg_tau is not None:
                if abs(tau_list[-i] - avg_tau) > 3 * std_tau:
                    processed.stable_since = dates[i_list[-i+2]]
                    break
            avg_tau = average(tau_list[-i:])
            std_tau = std(tau_list[-i:])

        if len(fit_list) > 24:
            errors = [fit.sum_error for fit in fit_list]
            processed.error_avg = average(errors[12:-12])
            errors = errors - processed.error_avg
            processed.error_std = std(errors)

        self.set_fit(last_good_fit)

        processed.save()

    def compute_fit(self):
        fit_list = list(self.processed.fits.filter(date_end__lt=self.date_max).order_by("date_end").all())

        if len(fit_list) == 0:
            return

        if len(fit_list) > 24:
            errors = [fit.sum_error for fit in fit_list]
            self.processed.error_avg = average(errors[12:-12])
            errors = errors - self.processed.error_avg
            self.processed.error_std = std(errors)

        self.set_fit(fit_list[-1])

        self.processed.save()

    def get_maximum(self):
        try:
            max_xs = argrelextrema(array(self.y_s), np.greater, order=24)[0]
            max_ys = [self.y_s[i] for i in max_xs]
            max_y = max(max_ys)
            max_x = list(max_ys).index(max_y)
            if max_ys[-1] != max_y and max_y < 1.5 * max_ys[-1]:
                max_x = -1
            dates = [self.dates[i] for i in max_xs]
            return dates[max_x]
        except Exception as e:
            print e
            return date(year=1900, month=1, day=1)

    @staticmethod
    def set_maximum(start_date, options):
        if options.get('start_year', 0) == 0 and options.get('start_month', 0) == 0:
            options['start_year'] = start_date.year
            options['start_month'] = start_date.month

    @abc.abstractmethod
    def get_stretched_exponential(self, processed, date_end):
        return

    def get_plot_data(self, options=None):
        start_year = 0
        start_month = 0

        if options is not None:
            start_year = int(options.get('start_year', 0))
            start_month = int(options.get('start_month', 0))

        first_date = self.productions[0].date
        dates, x, y = [], [], []
        for production in self.productions:
            if production.date.year > start_year or (production.date.year == start_year and
                                                     production.date.month >= start_month):
                dates.append(production.date)
                x.append(diff_months_abs(production.date, first_date))
                y.append(production.production_oil)

        return dates, x, y

    def set_fit(self, fit):
        if fit is not None:
            self.processed.date_begin = fit.date_begin
            self.processed.x_min = fit.x_min
            self.processed.A = fit.A
            self.processed.tau = fit.tau
            self.processed.beta = fit.beta

    @staticmethod
    def last_not_zero(numeric_array):
        for e in reversed(numeric_array):
            if e > 0:
                return e
        return 0

    def set_information(self):
        processed = self.processed
        productions = self.productions
        dates, y = self.dates, self.y_s

        # Only concerns fields, not countries
        if hasattr(processed, 'country'):
            processed.country = productions[0].country
            print "Serialize production"
            processed.production_oil = self.serialize_productions(productions)
        else:
            processed.production_oil = self.serialize_productions(
                self.production_type.objects.filter(name=processed.name).order_by("date").all()
            )
        print "Set discovery date"
        processed.discovery = productions[0].date
        print "Compute total production"
        processed.total_production_oil = sum(y) / 1.0E6
        if processed.total_production_oil > 1.0:
            processed.total_production_oil = round(processed.total_production_oil)
        print "Set active"
        processed.active = diff_months_abs(dates[-1], self.date_max) < 12
        if processed.active is True:
            processed.shut_down = None
            processed.current_production_oil = self.last_not_zero(y)
        else:
            processed.shut_down = dates[-1]
            processed.current_production_oil = 0

    @staticmethod
    def serialize_productions(productions):
        return serializers.serialize(
            "json",
            productions,
            fields=('date', 'production_oil')
        )

    @staticmethod
    def deserialize_productions(productions):
        return serializers.deserialize(
            "json",
            productions,
            fields=('date', 'production_oil')
        )


class FieldProcessor(ProductionProcessor):
    production_type = FieldProduction
    processed_type = Field

    def get_list(self, name):
        return FieldProduction.objects.filter(country=name).values("name").distinct()

    def get_stretched_exponential(self, processed, date_end):
        return StretchedExponential.objects.get_or_create(field=processed, date_end=date_end)


class CountryProcessor(ProductionProcessor):
    production_type = CountryProduction
    processed_type = Country
    fields = []

    def compute_item(self, options):
        print "Compute country item"
        ProductionProcessor.compute_item(self, options)

        forecasts = self.init_forecasts(self.processed.date_begin, 12 * 30)

        self.fields = Field.objects.filter(
            country=self.processed.name,
            discovery__lt=self.date_max,
        ).all()
        for field in self.fields:
            if field.error_avg != 0 and field.error_std != 0:
                self.forecast(field, forecasts)

        for forecast in forecasts:
            forecast['date'] = str(forecast['date'])
            if forecast['average'] > 0 and forecast['sigma'] > 0:
                forecast['sigma'] = sqrt(forecast['sigma']).real / forecast['average']
            print "{0}: {1} / {2}".format(
                forecast['date'],
                forecast['average'],
                forecast['sigma'],
            )

        self.processed.forecasts = json.dumps(forecasts)
        self.processed.save()

    @staticmethod
    def init_forecasts(start_date, number_month):
        return [{
            'date': add_months(start_date, n),
            'average': 0,
            'sigma': 0,
        } for n in range(0, number_month)]

    @staticmethod
    def forecast(field, forecasts):
        if not field.stable:
            return
        func = get_stretched_exponential(field.A, field.tau, field.beta)
        for forecast in forecasts:
            number_months = diff_months(field.date_begin, forecast['date'])
            if number_months <= 0:
                production = func(field.x_min - number_months) * (1 - field.error_avg)
                forecast['average'] += production
                forecast['sigma'] += (production * field.error_std)**2

    def forecast_recent(self, field, forecasts):
        pass

    def get_list(self, name):
        return CountryProduction.objects.filter(name=name).values("name").distinct()

    def get_stretched_exponential(self, processed, date_end):
        return StretchedExponential.objects.get_or_create(country=processed, date_end=date_end)
