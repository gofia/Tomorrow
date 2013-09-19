from django.db import models
from django.db.models import Max

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests, calendar, datetime
import logging


logger = logging.getLogger("BseeLoader")


class Production(models.Model):
    logger.info("Created production.")
    name = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    date = models.DateField(unique_for_date="name")
    production_oil = models.PositiveIntegerField(default=0)
    production_gas = models.PositiveIntegerField(null=True, default=None)
    depth = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return self.name + " ; " + self.country + " ; " + self.date.__str__() + " ; "


class BseeManager():
    update_to = datetime.date.today()

    def getOldestDate(self):
        last_date = Production.objects.all().aggregate(Max('date'))

        if last_date['date__max'] is None:
            return date(year=1947, month=11, day=1)

        return last_date['date__max']

    def update(self):
        logger.info("Bsee update started.")
        number_updates = 0
        bseeRequest = BseeRequest()
        bseeRequest.year_month = self.getOldestDate()
        while bseeRequest.year_month < self.update_to:
            productions = bseeRequest.getProductions()
            number_updates = number_updates + len(productions)
            for production in productions:
                production.save()
            bseeRequest.nextMonth()
        logger.info("Bsee update finished.")
        return number_updates


class BseeRequest():
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
        if page == 1:
            self.session = requests.session()
            r = self.session.post(self.url, data=self.getPostData())
        elif page > 1:
            r = self.session.post(self.url, data=self.getNextPagePostData(page))
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
            logger.error("Table is None.", )
            return productions

        trs = table.findAll('tr')

        if trs is None:
            logger.error("Rows are None.")
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
            logger.error("Row did not have 10 columns.")
            return None

        p = Production()
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