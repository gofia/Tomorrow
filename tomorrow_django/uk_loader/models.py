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

from django.db.models import Max, Sum

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests
import datetime
import logging

from oil_and_gas.models import WellProduction, FieldProduction

logger = logging.getLogger("UkLoader")


class UkManager():
    update_to = datetime.date.today()

    def __init__(self):
        pass

    @staticmethod
    def get_youngest_date(well_name):
        last_date = WellProduction.objects.all().filter(name=well_name).aggregate(Max('date'))

        if last_date['date__max'] is None:
            return date(year=1947, month=11, day=1)

        return last_date['date__max']

    def update(self, to_page):
        logger.info("Uk update started.")
        number_updates = 0
        uk_request = UkRequest()
        page = 0
        while page <= to_page or to_page is None:
            productions = uk_request.get_production_page(page)
            if productions == "End":
                break
            number_updates += len(productions)
            if len(productions) > 0:
                wel_name = productions[0].name
                youngest_date = self.get_youngest_date(wel_name)
                for production in productions:
                    if production.date > youngest_date:
                        production.save()
            page += 1
        logger.info("Uk update finished.")
        return number_updates


class UkAggregator():
    def __init__(self):
        pass

    @staticmethod
    def get_fields():
        return WellProduction.objects.filter(country="UK").values("field").distinct()

    @staticmethod
    def aggregate_wells(name):
        return WellProduction.objects.filter(field=name).values('date').annotate(
            total_oil=Sum('production_gas'),
            total_gas=Sum('production_oil'),
            total_water=Sum('production_water'),
        )

    @staticmethod
    def set_field_data(field, agg_well):
        field.name = agg_well['field']
        field.country = 'UK'
        field.date = agg_well['date']
        field.production_oil = agg_well['total_oil']
        field.production_gas = agg_well['total_gas']
        field.production_water = agg_well['total_water']

    def compute_fields(self, fields):
        for field in fields:
            field_name = field['field']
            agg_wells = self.aggregate_wells(field_name)
            for agg_well in agg_wells:
                agg_well['field'] = field_name
                production_date = agg_well['date']
                field_production, created = FieldProduction.objects.get_or_create(
                    name=field_name,
                    date=production_date
                )
                self.set_field_data(field_production, agg_well)
                field_production.save()
        return len(fields)

    def compute(self):
        fields = self.get_fields()
        return self.compute_fields(fields)


class UkRequest():
    url = "https://www.og.decc.gov.uk/information/wells/pprs/Well_production_offshore_oil_fields/offshore_oil_fields_by_well"
    session = None

    def __init__(self):
        pass

    def get_soup(self, page):
        self.session = requests.session()
        r = self.session.post(self.url + "/" + page.__str__() + ".htm")
        return BeautifulSoup(r.content)

    def get_production_page(self, page):
        productions = []
        soup = self.get_soup(page)
        names = soup.findAll('font', size=3, face="Arial")
        field_name = names[1].text
        well_name = names[2].text
        table = soup.find('table', width=490, border=1)

        if table is None:
            logger.error("Table is None.", )
            return "End"

        trs = table.findAll('tr')

        if trs is None:
            logger.error("Rows are None.")
            return productions

        trs = trs[1:]
        for row in trs:
            production = self.get_production(row)
            production.name = well_name
            production.field = field_name
            if production is not None:
                productions.append(production)

        return productions

    def get_production(self, row):
        tds_font = row.findAll('td')
        tds = []
        for td in tds_font:
            tds.append(td.find('font'))

        if len(tds) != 7:
            logger.error("Row did not have 7 columns.")
            print "Row did not have 7 columns."
            return None

        p = WellProduction()
        p.country = "UK"
        year = self.to_int_or_zero(tds[0].text)
        month = self.to_int_or_zero(tds[1].text)
        p.date = date(year=year, month=month, day=1)
        p.production_oil = self.to_int_or_zero(tds[2].text)
        p.production_gas = self.to_int_or_zero(tds[3].text)
        p.production_water = self.to_int_or_zero(tds[4].text)
        return p

    @staticmethod
    def to_int_or_zero(value):
        value = value.replace(",", "")
        try:
            int_value = int(value)
            return int_value
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0