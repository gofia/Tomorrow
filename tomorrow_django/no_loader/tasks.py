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

from .models import NoManager
import logging


logger = logging.getLogger("NoLoader")


@task()
def update_no():
    logger.info("Update No task started.")
    no_manager = NoManager()
    return no_manager.update()
