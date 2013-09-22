from django.db.models import Max, Sum

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests, datetime
import logging

from oil_and_gas.models import WellProduction, FieldProduction

logger = logging.getLogger("UkLoader")


class UkManager():
    update_to = datetime.date.today()

    def getYoungestDate(self, wellName):
        last_date = WellProduction.objects.all().filter(name=wellName).aggregate(Max('date'))

        if last_date['date__max'] is None:
            return date(year=1947, month=11, day=1)

        return last_date['date__max']

    def update(self, toPage):
        logger.info("Uk update started.")
        number_updates = 0
        ukRequest = UkRequest()
        page = 0
        while page <= toPage or toPage is None:
            productions = ukRequest.getProductionPage(page)
            if productions == "End":
                break;
            number_updates = number_updates + len(productions)
            if len(productions) > 0:
                wellName = productions[0].name
                youngestDate = self.getYoungestDate(wellName)
                for production in productions:
                    if production.date > youngestDate:
                        production.save()
            page = page + 1
        logger.info("Uk update finished.")
        return number_updates


class UkAggregator():
    def getFields(self):
        return WellProduction.objects.filter(country="UK").values("field").distinct()

    def aggregateWells(self, name):
        return WellProduction.objects.filter(field=name).values('date').annotate(
            total_oil=Sum('production_gas'),
            total_gas=Sum('production_oil'),
            total_water=Sum('production_water'),
        )

    def aggWellToField(self, agg_well):
        return FieldProduction(
            name=agg_well.field,
            country="UK",
            date=agg_well['date'],
            production_oil=agg_well['total_oil'],
            production_gas=agg_well['total_gas'],
            production_water=agg_well['total_water'],
        )

    def computeFields(self, fields):
        for field in fields:
            fieldName=field['field']
            agg_wells = self.aggregateField(fieldName)
            for agg_well in agg_wells:
                productionDate=agg_well['date']
                fieldProduction = FieldProduction.objects.get_or_create(name=fieldName, date=productionDate)
                self.setFieldData(fieldProduction, agg_well)
                fieldProduction.save()

class UkRequest():
    url = "https://www.og.decc.gov.uk/information/wells/pprs/Well_production_offshore_oil_fields/offshore_oil_fields_by_well"
    session = None

    def getSoup(self, page):
        self.session = requests.session()
        r = self.session.post(self.url + "/" + page.__str__() + ".htm")
        return BeautifulSoup(r.content)

    def getProductionPage(self, page):
        productions = []
        soup = self.getSoup(page)
        names = soup.findAll('font', size=3, face="Arial")
        fieldName = names[1].text;
        wellName = names[2].text;
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
            production = self.getProduction(row)
            production.name = wellName
            production.field = fieldName
            if production is not None:
                productions.append(production)

        return productions

    def getProduction(self, row):
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
        year = self.toIntOrZero(tds[0].text)
        month = self.toIntOrZero(tds[1].text)
        p.date = date(year=year, month=month, day=1)
        p.production_oil = self.toIntOrZero(tds[2].text)
        p.production_gas = self.toIntOrZero(tds[3].text)
        p.production_water = self.toIntOrZero(tds[4].text)
        return p

    def toIntOrZero(self, value):
        value = value.replace(",", "")
        try:
            intValue = int(value)
            return intValue
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0