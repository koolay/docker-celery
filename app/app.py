# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from celery import Celery
from dotenv import load_dotenv

from configs import redis_uri, mongo_uri
from tasks.task import BaseTask

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PROJECT_NAME = 'apicloud'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'

# app = Celery('tasks', broker='redis://:dev@redis:6379/1')

print 'connect redis: %s' % redis_uri
print 'connect mongo: %s' % mongo_uri

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

    print 'apiId: %s' % api_id
