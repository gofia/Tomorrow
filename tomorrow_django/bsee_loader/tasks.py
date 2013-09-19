__author__ = 'Lucas-Fievet'

from celery import task

from bsee_loader.models import BseeManager
import logging


logger = logging.getLogger("BseeLoader")


@task()
def updateBsee(date=None):
    logger.info("Update Bsee task started.")
    bseeManager = BseeManager()
    if date is not None:
        bseeManager.update_to = date
    return bseeManager.update()