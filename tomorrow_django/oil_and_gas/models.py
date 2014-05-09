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

from django.db import models
from django.db.models import Max
from datetime import datetime

import math

from fitting import fit_stretched_exponential, r_squared

import logging
from .fitting import get_stretched_exponential
from .utils import diff_months_abs

logger = logging.getLogger("OilAndGas")


class Production(models.Model):
    logger.info("Created production.")
    name = models.CharField(max_length=50, default="")
    date = models.DateField()

    # In BBL (barrels)
    production_oil = models.PositiveIntegerField(default=0)

    # In MCF (million cubic feet)
    production_gas = models.PositiveIntegerField(null=True, default=None)

    production_water = models.PositiveIntegerField(null=True, default=None)

    @property
    def production(self):
        return self.production_oil + (self.production_gas * 1000 / 5800)

    def __str__(self):
        return self.name + " ; " + self.date.__str__() + " ; "

    class Meta:
        abstract = True
        unique_together = (("name", "date"),)


class CountryProduction(Production):
    logger.info("Created country production.")

    def __str__(self):
        return self.name + " ; " + self.date.__str__() + " ; "


class FieldProduction(Production):
    logger.info("Created field production.")
    country = models.CharField(max_length=50, default="")
    depth = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return self.name + " ; " + self.country + " ; " + self.date.__str__() + " ; "


class Field(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    country = models.CharField(max_length=50, default="")
    discovery = models.DateField(null=True, blank=True)
    shut_down = models.DateField(null=True, blank=True)
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")
    total_production_oil = models.PositiveIntegerField(default=0)
    total_production_gas = models.PositiveIntegerField(default=0)
    current_production_oil = models.PositiveIntegerField(default=0)
    current_production_gas = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    stable = models.BooleanField(default=True)
    stable_since = models.DateField(null=True, blank=True)

    # A * exp((x/a)**b)
    date_begin = models.DateField(default=datetime.today())
    x_min = models.PositiveIntegerField(default=0)
    A = models.FloatField(default=0.0)
    tau = models.FloatField(default=-1.0)
    beta = models.FloatField(default=1.0)
    error_avg = models.FloatField(default=0.0, null=True)
    error_std = models.FloatField(default=0.0, null=True)

    @property
    def max_fits(self):
        max_date = self.fits.all().aggregate(Max('date_begin'))['date_begin__max']
        return self.fits.filter(date_begin=max_date).all()
    
    @property
    def extrapolated_total_production_oil(self):
        if not self.active:
            return self.total_production_oil * 1E6

        if not self.stable:
            return None

        extrapolated_production = self.total_production_oil * 1E6
        func = get_stretched_exponential(self.A, self.tau, self.beta)
        month_start = diff_months_abs(self.date_begin, datetime.now())
        for month in range(0, 12*25):
            production = func(self.x_min + month_start + month) * (1 - self.error_avg)
            extrapolated_production += production

        return extrapolated_production


class Country(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    discovery = models.DateField(null=True, blank=True)
    shut_down = models.DateField(null=True, blank=True)
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")
    total_production_oil = models.PositiveIntegerField(default=0)
    total_production_gas = models.PositiveIntegerField(default=0)
    current_production_oil = models.PositiveIntegerField(default=0)
    current_production_gas = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    stable = models.BooleanField(default=True)
    stable_since = models.DateField(null=True, blank=True)

    # A * exp((x/a)**b)
    date_begin = models.DateField(default=datetime.today())
    x_min = models.PositiveIntegerField(default=0)
    A = models.FloatField(default=0.0)
    tau = models.FloatField(default=-1.0)
    beta = models.FloatField(default=1.0)
    error_avg = models.FloatField(default=0.0, null=True)
    error_std = models.FloatField(default=0.0, null=True)

    forecasts = models.TextField(default="")

    @property
    def max_fits(self):
        max_date = self.fits.all().aggregate(Max('date_begin'))['date_begin__max']
        return self.fits.filter(date_begin=max_date).all()


class StretchedExponential(models.Model):
    # A * exp((x/a)**b)
    date_begin = models.DateField(default=datetime.today())
    date_end = models.DateField(default=datetime.today())
    x_min = models.PositiveIntegerField(default=0)
    length = models.PositiveIntegerField(default=0)
    A = models.FloatField(default=0.0)
    tau = models.FloatField(default=-1.0)
    beta = models.FloatField(default=1.0)
    field = models.ForeignKey(
        Field,
        null=True,
        default=None,
        related_name="fits"
    )
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        default=None,
        related_name="fits",
    )
    r_squared = models.FloatField(default=0)
    sum_error = models.FloatField(default=0)

    def compute_fit(self, x, y, x_min_guess=None, y0_guess=None, tau_guess=None, beta_guess=None):
        try:
            x_min, tau, beta, y0 = fit_stretched_exponential(
                x, y, x_min='max',
                x_min_guess=x_min_guess, y0=y0_guess, tau=tau_guess, beta=beta_guess
            )
        except Exception as e:
            print e
            return False

        if math.isnan(tau) or math.isnan(beta) or math.isnan(y0):
            return False

        self.x_min = x_min
        self.A = y0
        self.tau = tau
        self.beta = beta

        func = get_stretched_exponential(y0, tau, beta)
        x_min_index = x.index(x_min)
        self.r_squared = r_squared(func, x[x_min_index:-1], y[x_min_index:-1])
        return True

    def compute_error(self, x_s, y_s):
        try:
            func = get_stretched_exponential(self.A, self.tau, self.beta)
            extrapolated_total_production = sum(func(x_s))
            real_total_production = sum(y_s)
            error = extrapolated_total_production - real_total_production
            error /= real_total_production
            if error > 2:
                error = 0
            return error
        except ZeroDivisionError:
            return 0

    class Meta:
        unique_together = (("field", "date_begin", "date_end"),)


class DiscoveryScenario(models.Model):
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        default=None,
        related_name="discovery_scenarios",
    )
    probability = models.FloatField(default=0.0)
    pdf = models.FloatField(default=0.0)
    number_dwarfs = models.PositiveIntegerField(default=0)
    number_giants = models.PositiveIntegerField(default=0)
    probability_dwarf = models.FloatField(default=0.0)
    probability_giant = models.FloatField(default=0.0)

    def __str__(self):
        return "{0} - {1} - {2}/{3} - {4}/{5}".format(
            self.country.name,
            self.probability,
            self.number_dwarfs,
            self.number_giants,
            self.probability_dwarf,
            self.probability_giant,
        )
