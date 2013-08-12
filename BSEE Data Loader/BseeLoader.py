__author__ = 'lucas.fievet'

import requests
import csv
import time
from BeautifulSoup import BeautifulSoup

first = False

for year in range(2001, 2013):
    for month in range(1, 13):

        print year.__str__() + " " + month.__str__()

        URL = 'http://www.data.bsee.gov/homepg/data_center/production/production/prodlist.asp'
        postData = {
            'ch_prodmonth': 'on',
            'ch_prodyear': 'on',
            'fromm': "'" + month.__str__() + "'",
            'fromp': "'" + year.__str__() + "'",
            'order': 'ASC',
            'pagesize': '800',
            'sort': 'Production Year',
            'tom': "'" + month.__str__() + "'",
            'top': "'" + year.__str__() + "'"
        }

        session = requests.session()
        r = requests.post(URL, data=postData)

        soup = BeautifulSoup(r.content)

        table = soup.find('table', border=5, width=600)

        if table is not None:
            headers = table.findAll('th')[1:-1]
            if headers is not None:
                headers = [header.text for header in headers]

            rows = []
            trs = table.findAll('tr')
            if trs is not None:
                trs = trs[2:-1]
                for row in trs:
                    tds = row.findAll('td')
                    rows.append([val.text.encode('utf8') for val in tds])
                print "Found " + len(rows).__str__() + " rows"

            with open('C:\Users\lucas.fievet\Dropbox\PhD\Data\\bsee_data.csv', 'a') as f:
                writer = csv.writer(f)
                if first:
                    writer.writerow(headers)
                    first = False
                writer.writerows(row for row in rows if row)

        time.sleep(1)
