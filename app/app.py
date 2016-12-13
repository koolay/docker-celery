# -*- coding: utf-8 -*-
import os

from celery import Celery

from tasks.task import BaseTask

PROJECT_NAME = 'apicloud'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'

# app = Celery('tasks', broker='redis://:dev@redis:6379/1')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_db = os.environ.get('REDIS_DB')
redis_password = os.environ.get('REDIS_PASSWORD')

if redis_password:
    redis_uri = 'redis://:{3}@{0}:{1}/{2}'.format(redis_host, redis_port, redis_db, redis_password)
else:
    redis_uri = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)

app = Celery(broker=redis_uri)
app.conf.update(task_serializer='json')

# app.register_task(task.ProjectTestTask)
# app.register_task(task.APITestTask)

@app.task(base=BaseTask, name=u'%s.add.testing.project' % PROJECT_NAME)
def add_testing_project(project_id):
    """
    对项目所有接口自动化测试　
    :param project_id:
    :return:
    """

    print 'projectId: %s' % project_id

@app.task(base=BaseTask, name=u'%s.add.testing.api' % PROJECT_NAME)
def add_testing_api(api_id):
    """
    对接口自动化测试
    :param api_id:
    :return:
    """

    print 'apiId: %s' %api_id
