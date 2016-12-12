# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-12.
  summary
"""
import celery

class TestingTask(celery.Task):

    def __init__(self):
        self.name = 'testing'
        super.__init__()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print '{0!r} failed: {1!r}'.format(task_id, exc)