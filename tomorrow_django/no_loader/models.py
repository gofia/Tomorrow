from django.db.models import Max, Sum

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests, datetime
import socket
import logging

from oil_and_gas.models import FieldProduction

logger = logging.getLogger("NoLoader")


class NoManager():
    url = "http://factpages.npd.no/ReportServer?/FactPages/TableView/" \
          "field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:" \
          "Parameters=f&rs:Format=CSV&Top100=false&IpAddress={0}&CultureCode=en"

    def update(self):
        csv = self.getCsv()
        self.processCsv(csv)

    def getCsv(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
        s.close()
        r = requests.get(self.url.format(ip))
        return r.content

    def processCsv(self, csv):
        rows = csv.split('\n')
        for row in rows[1:-1]:
            self.processRow(row)

    def processRow(self, row):
        columns = row.split(",")

        if len(columns) != 10:
            return;

        field_name = columns[0]
        print field_name
        year = self.toIntOrZero(columns[1])
        print year
        month = self.toIntOrZero(columns[2])
        print month
        date =  date(year=year, month=month, day=1)
        p = FieldProduction.objects.get_or_create(name=field_name, country="NO", date=date)
        p.country = "NO"
        #year = self.toIntOrZero(tds[0].text)
        #month = self.toIntOrZero(tds[1].text)
        #p.date = date(year=year, month=month, day=1)
        #p.production_oil = self.toIntOrZero(tds[2].text)
        #p.production_gas = self.toIntOrZero(tds[3].text)
        #p.production_water = self.toIntOrZero(tds[4].text)
        return p

    def toIntOrZero(self, value):
        value = value.replace(",", "")
        try:
            intValue = int(value)
            return intValue
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0