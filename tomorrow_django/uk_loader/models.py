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

from oil_and_gas.models import FieldProduction

logger = logging.getLogger("UkLoader")


class UkManager():
    update_to = datetime.date.today()

    def __init__(self):
        pass

    @staticmethod
    def get_youngest_date(well_name):
        last_date = FieldProduction.objects.all().filter(name=well_name).aggregate(Max('date'))

        if last_date['date__max'] is None:
            return date(year=1947, month=11, day=1)

        return last_date['date__max']

    def update(self, to_page):
        logger.info("Uk update started.")
        if to_page is None:
            to_page = 290
        number_updates = 0
        uk_request = UkRequest()
        page = 0
        while page <= to_page:
            productions = uk_request.get_production_page(page)
            number_updates += len(productions)
            if len(productions) > 0:
                logger.error(productions[0].name)
                field_name = productions[0].name
                youngest_date = self.get_youngest_date(field_name)
                for production in productions:
                    if production.date > youngest_date:
                        production.save()
            page += 1
        logger.info("Uk update finished.")
        return number_updates


class UkRequest():
    url = "https://www.og.decc.gov.uk/pprs/full_production/oil+production+sorted+by+field"
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
        names = soup.findAll('td', {"class": "s5"})
        field_name = names[0].text
        table = soup.find('table', width="861", cellspacing="0")

        if table is None:
            logger.error("Table is None.", )
            return productions

        trs = table.findAll('tr')

        if trs is None:
            logger.error("Rows are None.")
            return productions

        trs = trs[1:]
        for row in trs:
            row_production = self.get_production(row, field_name)
            if row_production is not None:
                productions += row_production

        return productions

    def get_production(self, row, field_name):
        tds = row.findAll('td')

        if len(tds) != 14:
            logger.error("Row did not have 14 columns.")
            print "Row did not have 14 columns."
            return None

        productions = []
        for idx, td in enumerate(tds[1:13]):
            p = FieldProduction()
            p.country = "UK"
            p.name = field_name
            year = self.to_int_or_zero(tds[0].text)
            p.date = date(year=year, month=idx+1, day=1)
            p.production_oil = self.to_int_or_zero(td.text) * 6.2898
            productions.append(p)

        return productions

    @staticmethod
    def to_int_or_zero(value):
        value = value.replace(",", "")
        try:
            int_value = int(value)
            return int_value
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0
