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

from .models import UkManager
import logging


logger = logging.getLogger("UkLoader")


@task()
def update_uk(to_page=None):
    logger.info("Update UK task started.")
    uk_manager = UkManager()
    return uk_manager.update(to_page)
