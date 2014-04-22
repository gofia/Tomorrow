from django.db.models import Max
from django.db import IntegrityError

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests, calendar, datetime
from requests.adapters import HTTPAdapter
import logging

from oil_and_gas.models import FieldProduction

logger = logging.getLogger("UsLoader")


class UsManager():
    update_to = datetime.date.today()

    def getOldestDate(self):
        last_date = FieldProduction.objects.all().aggregate(Max('date'))

        if last_date['date__max'] is None:
            return date(year=1947, month=11, day=1)

        return last_date['date__max']

    def update(self):
        logger.error("US update started.")
        number_updates = 0
        usRequest = UsRequest()
        usRequest.year_month = self.getOldestDate()
        while usRequest.year_month < self.update_to:
            productions = usRequest.getProductions()
            number_updates = number_updates + len(productions)
            for production in productions:
                try:
                    production.save()
                except (IntegrityError,):
                    logger.error("Entry " + production.__str__() + " already exists")
            usRequest.nextMonth()
            logger.error("Added " + len(productions).__str__() + " new entries.")
        logger.error("US update finished with " + number_updates.__str__() + " new entries.")
        return number_updates


class UsRequest():
    url = "http://www.data.bsee.gov/homepg/data_center/production/production/prodlist.asp"
    year_month = date(year=1947, month=1, day=1)
    session = None

    def getPostData(self):
        return {
            'ch_prodmonth': 'on',
            'ch_prodyear': 'on',
            'fromm': "'" + self.year_month.month.__str__() + "'",
            'fromp': "'" + self.year_month.year.__str__() + "'",
            'order': 'ASC',
            'pagesize': '500',
            'sort': 'Production Year',
            'tom': "'" + self.year_month.month.__str__() + "'",
            'top': "'" + self.year_month.year.__str__() + "'"
        }

    def getNextPagePostData(self, page):
        return {
            'PageTo': "'" + page.__str__() + "'",
            'Paging': 'True',
            'sort' : 'Production Year',
            'strOption' : 'Production Year and Production Month'
        }

    def getSoup(self, page):
        r = None
        try :
            if page == 1:
                self.session = requests.session()
                self.session.mount('http://', HTTPAdapter(max_retries=5))
                r = self.session.post(self.url, data=self.getPostData())
            elif page > 1:
                r = self.session.post(self.url, data=self.getNextPagePostData(page))
        except:
            logger.error("Page was not accessible")
        return BeautifulSoup(r.content)

    def getProductions(self):
        page = 1
        productions = []
        pageProductions = []
        while len(pageProductions) > 0 or page == 1:
            pageProductions = self.getProductionPage(page)
            productions = productions + pageProductions
            page = page + 1

        return productions

    def getProductionPage(self, page):
        productions = []
        soup = self.getSoup(page)
        table = soup.find('table', border=5, width=600)

        if table is None:
            logger.warning("Table is None.", )
            return productions

        trs = table.findAll('tr')

        if trs is None:
            logger.warning("Rows are None.")
            return productions

        trs = trs[2:]
        for row in trs:
            production = self.getProduction(row)
            if production is not None:
                productions.append(production)

        return productions

    def getProduction(self, row):
        tds = row.findAll('td')
        if len(tds) != 10:
            logger.warning("Row did not have 10 columns.")
            logger.warning(row.__str__())
            return None

        p = FieldProduction()
        p.name = tds[0].text
        p.country = "US"
        month = self.toIntOrZero(tds[1].text)
        year = self.toIntOrZero(tds[2].text)
        p.date = date(year=year, month=month, day=1)
        p.production_oil = self.toIntOrZero(tds[3].text) + self.toIntOrZero(tds[5].text)
        p.production_gas = self.toIntOrZero(tds[4].text) + self.toIntOrZero(tds[6].text)
        p.depth = self.toIntOrZero(tds[9].text)
        return p

    def toIntOrZero(self, value):
        value = value.replace(",", "")
        try:
            intValue = int(value)
            return intValue
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0

    def nextMonth(self):
        month = self.year_month.month
        year = self.year_month.year + month / 12
        month = month % 12 + 1
        day = min(self.year_month.day, calendar.monthrange(year,month)[1])
        self.year_month = datetime.date(year,month,day)