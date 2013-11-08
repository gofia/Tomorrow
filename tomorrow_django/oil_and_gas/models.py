from django.db import models
from django.core import serializers
from django.db.models import Max
from dateutil import relativedelta
from datetime import datetime

import math

from fitting import fit_stretched_exponential, r_squared

import logging
from oil_and_gas.fitting import get_stretched_exponential

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


class WellProduction(Production):
    logger.info("Created well production.")
    field = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    depth = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return self.name + " ; " + self.country + " ; " + self.date.__str__() + " ; "


class Field(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    country = models.CharField(max_length=50, default="")
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")

    # A * exp((x/a)**b)
    x_min = models.PositiveIntegerField(default=0)
    A = models.FloatField(default=0.0)
    tau = models.FloatField(default=-1.0)
    beta = models.FloatField(default=1.0)

    @property
    def max_fits(self):
        max_date = self.fits.all().aggregate(Max('date_begin'))['date_begin__max']
        return self.fits.filter(date_begin=max_date).all()


class Country(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")

    # A * exp((x/a)**b)
    x_min = models.PositiveIntegerField(default=0)
    A = models.FloatField(default=0.0)
    tau = models.FloatField(default=-1.0)
    beta = models.FloatField(default=1.0)

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

    def compute_fit(self, x, y):
        try:
            x_min, tau, beta, y0 = fit_stretched_exponential(x, y, x_min='max')
        except:
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

    class Meta:
        unique_together = (("field", "date_begin", "date_end"),)