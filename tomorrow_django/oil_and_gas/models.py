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
        return self.fits.filter(date_begin = max_date).all()


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
        related_name="fits"
    )
    r_squared = models.FloatField(default=0)
    sum_error = models.FloatField(default=0)

    def compute_fit(self, x, y):
        x_min, tau, beta, y0 = fit_stretched_exponential(x, y, x_min='max')

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


class FieldProcessor():
    def getFields(self):
        return FieldProduction.objects.values("name").distinct()

    def compute(self):
        fields = self.getFields()
        return self.computeFields(fields)

    def computeFields(self, fields):
        for field in fields:
            name = field['name']
            self.computeField(name)
        return len(fields)

    def computeField(self, name):
        productions = FieldProduction.objects.filter(name=name).all().order_by('date')
        field, created = Field.objects.get_or_create(name=name)
        field.name = name
        field.country = productions[0].country
        serialized_productions = serializers.serialize("json", productions, fields=('date', 'production_oil'))
        field.production_oil = serialized_productions
        field.save()
        self.compute_fits(field, productions)

    def compute_fits(self, field, productions):
        dates, x, y = self.getPlotData(productions)
        fit = None

        for i in range(2, len(x)):
            fit, created = StretchedExponential.objects.get_or_create(field=field, date_end=dates[i])
            if fit.compute_fit(x[0:i], y[0:i]):
                try:
                    fit.date_begin = dates[0] + relativedelta.relativedelta(months=fit.x_min)
                    fit.date_end = dates[i]
                    fit.length = i
                    func = get_stretched_exponential(fit.A, fit.tau, fit.beta)
                    x_min_index = x.index(fit.x_min)
                    fit.sum_error = sum(y[x_min_index:-1]) - sum(func(x[x_min_index:-1]))
                    fit.field = field
                    fit.save()
                    print "SUCCESS: " + fit.field.name + " - " + \
                          fit.date_begin.__str__() + " - " + fit.date_end.__str__()
                except Exception as e:
                    print "EXCEPTION: " + e.__str__()
                    fit.delete()
            else:
                print "FAILURE"
                fit.delete()

        if fit is not None:
            field.x_min = fit.x_min
            field.A = fit.A
            field.tau = fit.tau
            field.beta = fit.beta
            field.save()

    def getPlotData(self, productions):
        first_date = productions[0].date
        dates, x, y = [], [], []
        for production in productions:
            time_delta = relativedelta.relativedelta(production.date, first_date)
            dates.append(production.date)
            x.append(time_delta.years * 12 + time_delta.months)
            y.append(production.production_oil)
        return dates, x, y


class Country(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")


class CountryAggregator():
    def getCountries(self):
        return FieldProduction.objects.values("country").distinct()

    def aggregateFields(self, name):
        return FieldProduction.objects.filter(country=name).values('date').annotate(
            total_oil=Sum('production_gas'),
            total_gas=Sum('production_oil'),
            total_water=Sum('production_water'),
        )

    def setCountryData(self, country, agg_well):
        country.name = agg_well['field']
        country.country = 'UK'
        country.date = agg_well['date']
        country.production_oil = agg_well['total_oil']
        country.production_gas = agg_well['total_gas']
        country.production_water = agg_well['total_water']

    def computeCountries(self, countries):
        for country in countries:
            country_name = country['country']
            Country, created = Country.objects.get_or_create(name=country_name)
            agg_fields = self.aggregateFields(country_name)
            for agg_field in agg_fields:
                agg_field['field'] = country_name
                productionDate = agg_field['date']
                self.setCountryData(Country, agg_field)
                Country.save()
        return len(fields)

    def compute(self):
        countries = self.getCountries()
        return self.computeCountry(countries)
