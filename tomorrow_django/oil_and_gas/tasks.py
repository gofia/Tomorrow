__author__ = 'Lucas-Fievet'

from celery import task

from oil_and_gas.models import FieldProcessor

import logging


logger = logging.getLogger("OilAndGas")


@task()
def process_fields(date=None):
    logger.info("Process fields.")
    fieldProcessor = FieldProcessor()
    return fieldProcessor.compute()