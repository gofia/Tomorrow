__author__ = 'Lucas-Fievet'

from celery import task

from us_loader.models import UsManager
import logging


logger = logging.getLogger("UsLoader")


@task()
def updateUs(date=None):
    logger.info("Update Us task started.")
    usManager = UsManager()
    if date is not None:
        usManager.update_to = date
    return usManager.update()