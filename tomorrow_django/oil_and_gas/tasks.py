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

from celery import task

from .processing import FieldProcessor, CountryProcessor
from .aggregation import CountryAggregator

import logging


logger = logging.getLogger("OilAndGas")


@task()
def process_fields(country="NO"):
    logger.info("Process fields.")
    field_processor = FieldProcessor()
    return field_processor.compute(country)


@task()
def process_field(options):
    logger.info("Process field " + options['name'])
    field_processor = FieldProcessor()
    return field_processor.compute_item(options)


@task()
def process_countries(country="NO"):
    logger.info("Process countries.")
    country_processor = CountryProcessor()
    return country_processor.compute(country)


@task()
def aggregate_countries(country="NO"):
    logger.info("Aggregate fields to country.")
    aggregator = CountryAggregator()
    return aggregator.compute([{'country': country}])
