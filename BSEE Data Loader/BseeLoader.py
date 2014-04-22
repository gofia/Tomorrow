__author__ = 'lucas.fievet'

import requests
import csv
import time
from BeautifulSoup import BeautifulSoup


def pageToCsv(soup, writeHeader):
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
                columns = [val.text.encode('utf8') for val in tds]
                if len(columns) > 0:
                    rows.append([val.text.encode('utf8') for val in tds])
            print "Found " + len(rows).__str__() + " rows"

        with open('D:\Dropbox\PhD\Data\\bsee_data_new.csv', 'a') as f:
            writer = csv.writer(f)
            if writeHeader:
                writeHeader = False
                writer.writerow(headers)
            writer.writerows(row for row in rows if row)

        return len(rows), writeHeader
    return 0, writeHeader


writeHeader = True


for year in range(2013, 2014):
    for month in range(1, 9):
        page = 1
        print year.__str__() + " " + month.__str__() + " " + page.__str__()

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
        r = session.post(URL, data=postData)

        soup = BeautifulSoup(r.content)
        numberRows, writeHeader = pageToCsv(soup, writeHeader)

        while numberRows > 0:
            page = page + 1
            print year.__str__() + " " + month.__str__() + " " + page.__str__()

            pagingPostData = {
                'PageTo': "'" + page.__str__() + "'",
                'Paging': 'True',
                'sort' : 'Default Sort',
                'strOption' : 'Production Year and Production Month'
            }
            r = session.post(URL, data=pagingPostData)

            soup = BeautifulSoup(r.content)
            numberRows, writeHeader = pageToCsv(soup, writeHeader)

            time.sleep(0.25)

