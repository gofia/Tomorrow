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

from django.db.models import Sum

from oil_and_gas.models import FieldProduction, CountryProduction


class CountryAggregator():
    def __init__(self):
        pass

    def compute(self, countries=None):
        if countries is None:
            countries = self.get_countries()
        return self.compute_countries(countries)

    @staticmethod
    def get_countries():
        return FieldProduction.objects.values("country").distinct()

    def compute_countries(self, countries):
        for country in countries:
            country_name = country['country']
            self.compute_country_productions(country_name)
        return len(countries)

    def compute_country_productions(self, name):
        agg_fields = self.aggregate_fields(name)
        for agg_field in agg_fields:
            production_date = agg_field['date']
            country_production, created = CountryProduction.objects.get_or_create(
                name=name,
                date=production_date,
            )
            self.set_country_data(country_production, agg_field)
            country_production.save()

    @staticmethod
    def aggregate_fields(name):
        return FieldProduction.objects.filter(country=name).values('date').annotate(
            total_oil=Sum('production_oil'),
            total_gas=Sum('production_gas'),
            total_water=Sum('production_water'),
        )

    @staticmethod
    def set_country_data(country_production, agg_production):
        country_production.production_oil = agg_production['total_oil']
        country_production.production_gas = agg_production['total_gas']
        country_production.production_water = agg_production['total_water']