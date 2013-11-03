__author__ = 'Lucas-Fievet'

from celery import task

from no_loader.models import NoManager
import logging


logger = logging.getLogger("NoLoader")


@task()
def updateNo():
    logger.info("Update No task started.")
    noManager = NoManager()
    return noManager.update()