# -*- coding: utf-8 -*-
import datetime
from bson import ObjectId
from dotenv import load_dotenv
from os.path import join, dirname
import requests

from store.mongo import db

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from store.apicloud import get_testCase_by_project
from celery import Celery
from configs import redis_uri, mongo_uri
from tasks.task import BaseTask

PROJECT_NAME = 'apicloud'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'

# app = Celery('tasks', broker='redis://:dev@redis:6379/1')

print 'connect redis: %s' % redis_uri
print 'connect mongo: %s' % mongo_uri

app = Celery(broker=redis_uri)
app.conf.update(task_serializer='json')

ids = get_testCase_by_project('5812ee4bb914b20948209412')
for id in ids:
    print id['summary'].encode('utf-8')


# app.register_task(task.ProjectTestTask)
# app.register_task(task.APITestTask)

@app.task(base=BaseTask, name=u'%s.testing.project' % PROJECT_NAME)
def testing_project(task_id, project_id):
    """
    对项目所有接口自动化测试　
    :param task_id: 测试任务id
    :param project_id: 项目id
    :return:
    """

    if not project_id or not task_id:
        return

    for path in db.paths.find({'projectId': project_id}, {'_id': 1}):
        for mock in db.mocks.find({'pathId': str(path['_id'])}):
            testing_api(task_id, str(mock['_id']))

@app.task(base=BaseTask, name=u'%s.testing.api' % PROJECT_NAME)
def testing_api(task_id, testCase_id):
    """
    对接口自动化测试
    :param task_id:
    :param testCase_id: 测试用例id, 等同于mocks._id
    :return:
    """

    if not testCase_id or not task_id:
        return

    mock = db.mocks.find({'_id': ObjectId(testCase_id)})
    start = datetime.datetime.now()
    process = {
                'taskId': task_id, 'testCaseId': str(testCase_id),
               'requestOn': start,
               'responseOn': None,
               'summary': mock['summary'],
               'pathId': mock['pathId'],
               'path': mock['path'],
               'method': mock['method'],
               'headers': mock['headers'],
               'cookies': mock['cookies'],
               'query': mock['query'],
               'body': mock['body'],
               'consumes': mock['consumes'][0] if mock['consumes'] and len(mock['consumes']) else 'application/json'
               #'response': None,
               }



