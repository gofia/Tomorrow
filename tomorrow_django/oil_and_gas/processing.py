__author__ = 'lucas.fievet'

from django.core import serializers
from dateutil import relativedelta
import abc

from oil_and_gas.models import (Field, FieldProduction,
                                Country, CountryProduction,
                                StretchedExponential)
from oil_and_gas.fitting import get_stretched_exponential


class ProductionProcessor():
    production_type = None
    processed_type = None

    def compute(self, name):
        list = self.getList(name)
        return self.computeAll(list)

    @abc.abstractmethod
    def getList(self, name):
        return

    def computeAll(self, list):
        for item in list:
            name = item['name']
            self.computeItem(name)
        return len(list)

    def computeItem(self, name):
        productions = self.production_type.objects.filter(name=name).all().order_by('date')
        processed, created = self.processed_type.objects.get_or_create(name=name)
        processed.name = name
        processed.country = productions[0].country
        serialized_productions = serializers.serialize(
            "json",
            productions,
            fields=('date', 'production_oil')
        )
        processed.production_oil = serialized_productions
        processed.save()
        self.compute_fits(processed, productions)

    def compute_fits(self, processed, productions):
        dates, x, y = self.getPlotData(productions)
        fit = None

        for i in range(2, len(x)):
            fit, created = self.getStretchedExponential(processed, dates[i])
            if fit.compute_fit(x[0:i], y[0:i]):
                try:
                    fit.date_begin = dates[0] + relativedelta.relativedelta(months=fit.x_min)
                    fit.length = i

                    # Compute error
                    try:
                        func = get_stretched_exponential(fit.A, fit.tau, fit.beta)
                        extrapolated_total_production = sum(func(x[i:-1]))
                        real_total_production = sum(y[i:-1])
                        error = extrapolated_total_production - real_total_production
                        error /= real_total_production
                        fit.sum_error = error
                    except ZeroDivisionError:
                        pass

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
            processed.x_min = fit.x_min
            processed.A = fit.A
            processed.tau = fit.tau
            processed.beta = fit.beta
            processed.save()

    @abc.abstractmethod
    def getStretchedExponential(self, processed, date_end):
        return

    def getPlotData(self, productions):
        first_date = productions[0].date
        dates, x, y = [], [], []
        for production in productions:
            time_delta = relativedelta.relativedelta(production.date, first_date)
            dates.append(production.date)
            x.append(time_delta.years * 12 + time_delta.months)
            y.append(production.production_oil)
        return dates, x, y


class FieldProcessor(ProductionProcessor):
    production_type = FieldProduction
    processed_type = Field

    def getList(self, name):
        return FieldProduction.objects.filter(country=name).values("name").distinct()

    def getStretchedExponential(self, processed, date_end):
        return StretchedExponential.objects.get_or_create(field=processed, date_end=date_end)


class CountryProcessor(ProductionProcessor):
    production_type = CountryProduction
    processed_type = Country

    def getList(self, name):
        return CountryProduction.objects.filter(name=name).values("name").distinct()

    def getStretchedExponential(self, processed, date_end):
        return StretchedExponential.objects.get_or_create(country=processed, date_end=date_end)