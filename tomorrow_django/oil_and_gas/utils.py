import calendar
import datetime

__author__ = 'Lucas-Fievet'


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day,calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)