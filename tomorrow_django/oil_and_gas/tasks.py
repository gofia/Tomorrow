__author__ = 'Lucas-Fievet'

from celery import task

from oil_and_gas.processing import FieldProcessor, CountryProcessor
from oil_and_gas.aggregation import CountryAggregator

import logging


logger = logging.getLogger("OilAndGas")


@task()
def process_fields(date=None):
    logger.info("Process fields.")
    fieldProcessor = FieldProcessor()
    return fieldProcessor.compute("NO")


@task()
def process_field(name):
    logger.info("Process field " + name)
    fieldProcessor = FieldProcessor()
    return fieldProcessor.computeItem(name)


@task()
def process_countries(date=None):
    logger.info("Process countries.")
    countryProcessor = CountryProcessor()
    return countryProcessor.compute("NO")


@task()
def aggregate_countries(date=None):
    logger.info("Aggregate fields to country.")
    aggregator = CountryAggregator()
    return aggregator.compute([{'country': 'NO'}])