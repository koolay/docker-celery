# -*- coding: utf-8 -*-

from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/1')

print 'abc'