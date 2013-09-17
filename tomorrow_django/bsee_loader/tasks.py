__author__ = 'Lucas-Fievet'

from celery import task

from bsee_loader.models import BseeManager

@task()
def updateBsee():
    #bseeManager = BseeManager()
    #return bseeManager.update()
    return 1 + 1