__author__ = 'lucas.fievet'

from django.core import serializers
from dateutil import relativedelta

from oil_and_gas.models import Field, FieldProduction, StretchedExponential
from oil_and_gas.fitting import get_stretched_exponential


class FieldProcessor():
    def getFields(self, country):
        return FieldProduction.objects.filter(country=country).values("name").distinct()

    def compute(self, country):
        fields = self.getFields(country)
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
