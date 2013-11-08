__author__ = 'lucas.fievet'

from django.db.models import Sum

from oil_and_gas.models import FieldProduction, CountryProduction


class CountryAggregator():
    def compute(self, countries=None):
        if countries is None:
            countries = self.getCountries()
        return self.computeCountries(countries)

    def getCountries(self):
        return FieldProduction.objects.values("country").distinct()

    def computeCountries(self, countries):
        for country in countries:
            country_name = country['country']
            self.computeCountryProductions(country_name)
        return len(countries)

    def computeCountryProductions(self, name):
        agg_fields = self.aggregateFields(name)
        for agg_field in agg_fields:
            production_date = agg_field['date']
            countryProduction, created = CountryProduction.objects.get_or_create(
                name=name,
                date=production_date,
            )
            self.setCountryData(countryProduction, agg_field)
            countryProduction.save()

    def aggregateFields(self, name):
        return FieldProduction.objects.filter(country=name).values('date').annotate(
            total_oil=Sum('production_oil'),
            total_gas=Sum('production_gas'),
            total_water=Sum('production_water'),
        )

    def setCountryData(self, countryProduction, agg_production):
        countryProduction.production_oil = agg_production['total_oil']
        countryProduction.production_gas = agg_production['total_gas']
        countryProduction.production_water = agg_production['total_water']