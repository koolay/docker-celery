# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-12.
  summary
"""
import traceback

from celery import Task

class BaseTask(Task):

    def on_success(self, task_progress, task_id, args, kwargs):
        print 'Task %s: success returned with progress: %s', task_id, task_progress

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print u'Task %s: failure returned', task_id
        # print {"id": task_id, "exc": traceback.format_exc()}
