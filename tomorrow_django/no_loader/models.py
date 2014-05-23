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

from datetime import date
import requests
import socket
import logging
import re

from oil_and_gas.models import FieldProduction

logger = logging.getLogger("NoLoader")


class NoManager():
    url = "http://factpages.npd.no/ReportServer?/FactPages/TableView/" \
          "field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:" \
          "Parameters=f&rs:Format=CSV&Top100=false&IpAddress={0}&CultureCode=en"

    def __init__(self):
        pass

    def update(self, number_rows=-1):
        csv = self.get_csv()
        return self.process_csv(csv, number_rows)

    def get_csv(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        ip = s.getsockname()[0]
        s.close()
        r = requests.get(self.url.format(ip))
        return r.content

    def process_csv(self, csv, number_rows=-1):
        rows = csv.split('\n')
        for row in rows[1:number_rows]:
            self.process_row(row)
        return len(rows[1:number_rows])

    def process_row(self, row):
        columns = row.split(",")

        if len(columns) != 10:
            return

        field_name = columns[0]
        year = self.to_int_or_zero(columns[1])
        month = self.to_int_or_zero(columns[2])
        production_date = date(year=year, month=month, day=1)
        p, created = FieldProduction.objects.get_or_create(name=field_name, country="NO", date=production_date)
        p.production_oil = self.to_positive_float_or_zero(columns[3]) * 1E6 * 6.2898
        p.production_gas = self.to_positive_float_or_zero(columns[4]) * 1E6
        p.production_water = self.to_positive_float_or_zero(columns[8]) * 1E6
        p.save()

    @staticmethod
    def remove_special_characters(s):
        s = s.decode('utf-8')
        s = re.sub(r'\xc5', 'O', s)
        s = re.sub(r'\xd8', 'O', s)
        return s.encode('utf-8')

    @staticmethod
    def to_int_or_zero(value):
        value = value.replace(",", "")
        try:
            int_value = int(value)
            return int_value
        except:
            logger.error("Value " + value + " could not be converted to int.")
            return 0

    @staticmethod
    def to_positive_float_or_zero(value):
        value = value.replace(",", "")
        try:
            float_value = float(value)
            if float_value < 0:
                float_value = 0
            return float_value
        except:
            logger.error("Value " + value + " could not be converted to float.")
            return 0
