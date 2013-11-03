from django.db.models import Max, Sum

from datetime import date
from BeautifulSoup import BeautifulSoup
import requests, datetime
import socket
import logging
import re

from oil_and_gas.models import FieldProduction

logger = logging.getLogger("NoLoader")


class NoManager():
    url = "http://factpages.npd.no/ReportServer?/FactPages/TableView/" \
          "field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:" \
          "Parameters=f&rs:Format=CSV&Top100=false&IpAddress={0}&CultureCode=en"

    def update(self, number_rows=-1):
        csv = self.getCsv()
        return self.processCsv(csv, number_rows)

    def getCsv(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
        s.close()
        r = requests.get(self.url.format(ip))
        return r.content

    def processCsv(self, csv, number_rows=-1):
        rows = csv.split('\n')
        for row in rows[1:number_rows]:
            self.processRow(row)
        return len(rows[1:number_rows])

    def processRow(self, row):
        columns = row.split(",")

        if len(columns) != 10:
            return;

        field_name = columns[0]
        year = self.toIntOrZero(columns[1])
        month = self.toIntOrZero(columns[2])
        production_date = date(year=year, month=month, day=1)
        p, created = FieldProduction.objects.get_or_create(name=field_name, country="NO", date=production_date)
        p.production_oil = self.toPositiveFloatOrZero(columns[3]) * 1E6 * 8.3864
        p.production_gas = self.toPositiveFloatOrZero(columns[4]) * 1E6
        p.production_water = self.toPositiveFloatOrZero(columns[8]) * 1E6
        p.save()

    def remove_special_characters(self, s):
        s = s.decode('utf-8')
        s = re.sub(r'\xc5', 'O', s)
        s = re.sub(r'\xd8', 'O', s)
        return s.encode('utf-8')

    def toIntOrZero(self, value):
        value = value.replace(",", "")
        try:
            intValue = int(value)
            return intValue
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0

    def toPositiveFloatOrZero(self, value):
        value = value.replace(",", "")
        try:
            floatValue = float(value)
            if floatValue < 0:
                floatValue = 0
            return floatValue
        except:
            logger.error("Value " + value + " could not be converted to float.")
            return 0