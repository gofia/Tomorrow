__author__ = 'Lucas-Fievet'

from celery import task

from uk_loader.models import UkManager
import logging


logger = logging.getLogger("UkLoader")


@task()
def updateUk(toPage=None):
    logger.info("Update UK task started.")
    ukManager = UkManager()
    return ukManager.update(toPage)

@task()
def aggregateUk(fields=None):
    logger.info("Aggregate all UK wells into fields.")
    ukAggregator = UkAggregator()
    if field is None:
        return ukAggregator.compute()
    else:
        return ukAggregator.compute_all(fields)


@task()
def aggregateAndUpdateUk(fields=None):
    logger.info("Update and aggregate all UK wells.")
    result = updateUk.delay()
    if result.get() > 0:
        aggregateUk.delay()
