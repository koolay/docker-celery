# -*- coding: utf-8 -*-

from celery import Task
import logging
logger = logging.getLogger(__name__)

class BaseTask(Task):
    """Abstract base class for all tasks in my app."""

    abstract = True

    def on_success(self, task_progress, task_id, args, kwargs):
        msg = 'Task %s: success returned!' % task_id
        logger.debug(msg)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(exc.message)
