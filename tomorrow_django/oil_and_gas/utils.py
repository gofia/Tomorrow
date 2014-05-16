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
import matplotlib.pyplot as plt


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


def make_plot(x, y, x_label, y_label, x_fit=None, y_fit=None):
    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'ok')
    if x_fit is not None and y_fit is not None:
        ax.plot(x_fit, y_fit, '-k')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def start_plot(x_label, y_label, title):
    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(111)
    plt.title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return plt
