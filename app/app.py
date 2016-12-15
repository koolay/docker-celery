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
logger = logging.getLogger(__name__)

# app = Celery('tasks', broker='redis://:dev@redis:6379/1')

logger.debug('connect redis: %s' % redis_uri)
logger.debug('connect mongo: %s' % mongo_uri)

app = Celery(broker=redis_uri)
app.conf.update(task_serializer='json')


@app.task(base=BaseTask, name=u'%s.testing.project' % PROJECT_NAME)
def testing_project(task_id, project_id):
    """
    对项目所有接口自动化测试　
    :param task_id: 测试任务id
    :param project_id: 项目id
    :return:
    """

    logger.info('testing project with: %s, %s' % (task_id, project_id))

    if not project_id or not task_id:
        return

    config = apiCloudStore.get_config_by_project(project_id)
    if not config:
        logger.error(u'缺少db配置')
        return

    if not exec_sql(task_id, project_id, config):
        return

    amount_of_test = 0
    db.testtasks.update({'_id': ObjectId(task_id)}, {'$set': {'taskBegin': datetime.datetime.now()}})
    for path in db.paths.find({'projectId': project_id}, {'_id': 1}):
        for mock in db.mocks.find({'pathId': str(path['_id']), 'isTestCase': True}):
            amount_of_test += 1
            testing_api(task_id, str(mock['_id']), config)

    # 更新测试用例数目
    if amount_of_test > 0:
        db.testtasks.update({'_id': ObjectId(task_id)}, {'$set': {'testCaseCount': amount_of_test}})

def exec_sql(task_id, project_id, config):

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
    """
    批量测试
    :param task_id:
    :param testCase_ids:
    :param config:
    :return:
    """
    if not task_id or type(testCase_ids) != list or len(testCase_ids) < 1:
        logger.error(u'参数为空')
        return

    config = apiCloudStore.get_config_by_task(task_id)
    if not config:
        logger.error(u'缺少db配置')
        return

    task = db.testtask.find_one({'_id': ObjectId(task_id)})
    if not task:
        logger.error(u'task_id: %s 不存在' % task_id)
        return

    if not exec_sql(task_id, task['projectId'], config):
        return

    for testCase_id in testCase_ids:
        testing_api(task_id, testCase_id, config)


@app.task(base=BaseTask, name=u'%s.testing.api' % PROJECT_NAME)
def testing_api(task_id, testCase_id, config=None):
    """
    对接口自动化测试
    :param config:
    :param task_id:
    :param testCase_id: 测试用例id, 等同于mocks._id
    :return:
    """
    logger.info('received: %s, %s' % (task_id, testCase_id))
    if not testCase_id or not task_id:
        return
    if not config:
        config = apiCloudStore.get_config_by_task(task_id)

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
        'response': {}
    }

    payload = process['body'] if process['body'] else None
    headers = process['headers']
    params = process['query']
    cookies = process['cookies']
    url = '%s/%s' % (config['host'].rstrip('/'), process['path'].lstrip('/'))
    try:
        r = requests.request(process['method'], url,
                             data=payload,
                             headers=headers,
                             params=params,
                             cookies=cookies,
                             allow_redirects=False,
                             timeout=http_timeout
                             )

    except  requests.exceptions.RequestException as e:
        logger.info(u'请求%s出现异常: %s' % (process['path'], e.message))
        process['responseOn'] = datetime.datetime.now()
        process['response']['httpError'] = e.__str__()
        process['isExpected'] = False
        db.testtaskprocesses.insert_one(process)
        return

    except Exception as e:
        logger.exception(e)
        process['response']['httpError'] = e.message
        process['isExpected'] = False
        db.testtaskprocesses.insert_one(process)
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

    db.testtaskprocesses.insert_one(process)
    return
