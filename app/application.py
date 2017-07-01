# -*- coding: utf-8 -*-

from celery import Celery
import settings

rbkd = 'redis://%s:%d/%d' % (settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)

app = Celery('snh',
             broker=rbkd,
             backend=rbkd,
             include=['app.tasks.push'])

app.conf.update(task_serializer='json')
