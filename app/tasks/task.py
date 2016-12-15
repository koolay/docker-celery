# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-12.
  summary
"""
import logging
from celery import Task

logger = logging.getLogger(__name__)

class BaseTask(Task):

    def on_success(self, task_progress, task_id, args, kwargs):
        logger.debug('Task %s: success returned with progress: %s' % (task_id, task_progress))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.debug(u'Task %s: failure returned' % task_id)
