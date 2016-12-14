# -*- coding: utf-8 -*-
import datetime
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 保持在load_dotenv后面
from store import apicloud as apiCloudStore

import requests
import logging
from bson import ObjectId

from store.mongo import db

from celery import Celery
from configs import redis_uri, mongo_uri, http_timeout
from tasks.task import BaseTask

PROJECT_NAME = 'apicloud'

# app = Celery('tasks', broker='redis://:dev@redis:6379/1')

print 'connect redis: %s' % redis_uri
print 'connect mongo: %s' % mongo_uri

app = Celery(broker=redis_uri)
app.conf.update(task_serializer='json')

logger = logging.getLogger(__name__)


@app.task(base=BaseTask, name=u'%s.testing.project' % PROJECT_NAME)
def testing_project(task_id, project_id):
    """
    对项目所有接口自动化测试　
    :param task_id: 测试任务id
    :param project_id: 项目id
    :return:
    """

    print 'testing project with: %s, %s' % (task_id, project_id)

    if not project_id or not task_id:
        return

    if not exec_sql(task_id, project_id):
        return

    for path in db.paths.find({'projectId': project_id}, {'_id': 1}):
        print 'found path: %s' % str(path['_id'])
        for mock in db.mocks.find({'pathId': str(path['_id']), 'isTestCase': True}):
            testing_api(task_id, str(mock['_id']))


def exec_sql(task_id, project_id):
    config = apiCloudStore.get_config_by_project(project_id)
    if not config:
        logger.error(u'缺少db配置')
        return

    beforeSql = False
    beforeSqlScript = None
    # 暂时未实现, 需要使用group
    afterSql = False
    afterSqlScript = None

    if config.get('db') and config.get('db')['host']:
        sql = apiCloudStore.get_sql_by_project(project_id)
        if sql:
            beforeSqlScript = sql.get('beforeSql')
            afterSqlScript = sql.get('afterSql')
            beforeSql = True if beforeSqlScript else False
            afterSql = True if afterSqlScript else False

    if beforeSql:
        conn_options = config.get('db')
        try:

            apiCloudStore.exec_sql(beforeSqlScript, host=conn_options['host'], port=conn_options['port'],
                                   user=conn_options['username'], password=conn_options['password'])
        except Exception as e:
            logger.exception(e)
            apiCloudStore.update_task_error(task_id, e.message)
            return False
    return True


@app.task(base=BaseTask, name=u'%s.testing.apis' % PROJECT_NAME)
def testing_apis(task_id, testCase_ids):
    if not task_id or type(testCase_ids) != list or len(testCase_ids) < 1:
        logger.error(u'参数为空')
        return

    task = db.testtask.find_one({'_id': ObjectId(task_id)})
    if not task:
        logger.error(u'task_id: %s 不存在' % task_id)
        return

    if not exec_sql(task_id, task['projectId']):
        return

    for testCase_id in testCase_ids:
        testing_api(task_id, testCase_id)


@app.task(base=BaseTask, name=u'%s.testing.api' % PROJECT_NAME)
def testing_api(task_id, testCase_id):
    """
    对接口自动化测试
    :param task_id:
    :param testCase_id: 测试用例id, 等同于mocks._id
    :return:
    """
    print 'received: %s, %s' % (task_id, testCase_id)
    if not testCase_id or not task_id:
        return

    mock = db.mocks.find_one({'_id': ObjectId(testCase_id)})
    start = datetime.datetime.now()
    process = {
        'taskId': task_id, 'testCaseId': str(testCase_id),
        'requestOn': start,
        'responseOn': None,
        'summary': mock.get('summary'),
        'pathId': mock.get('pathId'),
        'path': mock.get('path'),
        'method': mock.get('method'),
        'headers': mock.get('headers'),
        'cookies': mock.get('cookies'),
        'query': mock.get('query'),
        'body': mock.get('body'),
        'consumes': mock.get('consumes')[0] if mock.get('consumes') and len(
            mock.get('consumes')) > 0 else 'application/json',
        'response': {},
    }

    payload = process['body'] if process['body'] else None
    headers = process['headers']
    params = process['query']
    cookies = process['cookies']

    try:
        r = requests.request(process['method'], process['path'],
                             data=payload,
                             headers=headers,
                             params=params,
                             cookies=cookies,
                             allow_redirects=False,
                             timeout=http_timeout
                             )

    except  requests.exceptions.RequestException as e:
        print u'请求%s出现异常: %s' % (process['path'], e.message)
        process['response']['httpError'] = e.message
        process['isExpected'] = False
        db.testTaskProcess.insert_one(process)
        return

    except Exception as e:
        print u'应用程序错误: %s' % e.message
        process['response']['httpError'] = e.message
        process['isExpected'] = False
        db.testTaskProcess.insert_one(process)
        return

    body = r.text
    process['responseOn'] = datetime.datetime.now()
    response = {
        'code': r.status_code,
        'headers': r.headers,
        'data': body
    }
    process['response'] = response

    #### 比较响应值是否一致
    expected = mock.get('httpCode') == response['code'] \
               and mock.get('resHeaders') == response['headers'] \
               and mock.get('body') == body

    process['response']['isExpected'] = expected

    db.testTaskProcess.insert_one(process)
    return
