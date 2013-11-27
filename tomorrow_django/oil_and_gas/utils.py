import calendar
import datetime

__author__ = 'Lucas-Fievet'


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day,calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def traverse(item, indices=[]):
    try:
        indices.append(0)
        for idx, i in enumerate(item):
            indices[-1] = idx
            for j, indices in traverse(i, indices):
                yield j, indices
        indices.pop()
    except:
        indices.pop()
        yield item, indices


def list_get(list, indices):
    results = []
    for item in list:
        for index in indices:
            item = item[index]
        results.append(item)
    return results
