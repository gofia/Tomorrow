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