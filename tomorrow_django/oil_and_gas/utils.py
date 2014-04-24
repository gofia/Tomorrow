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

import calendar
import datetime
from dateutil import relativedelta


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
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


def list_get(items, indices):
    results = []
    for item in items:
        for index in indices:
            item = item[index]
        results.append(item)
    return results


def diff_months(date1, date2):
    time_delta = relativedelta.relativedelta(date1, date2)
    return time_delta.years * 12 + time_delta.months


def diff_months_abs(date1, date2):
    return abs(diff_months(date1, date2))
