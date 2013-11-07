__author__ = 'Lucas-Fievet'

from celery import task

from oil_and_gas.processing import FieldProcessor
from oil_and_gas.aggregation import CountryAggregator

import logging


logger = logging.getLogger("OilAndGas")


@task()
def process_fields(date=None):
    logger.info("Process fields.")
    fieldProcessor = FieldProcessor()
    return fieldProcessor.compute()


@task()
def aggregate_countries(date=None):
    logger.info("Aggregate fields to country.")
    aggregator = CountryAggregator()
    return aggregator.compute([{'country': 'NO'}])