# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""
from bson import ObjectId

from store.mongo import db
from store.mysql import SimpleMysql

DEFAULT_ENV = 'test'


def update_task_error(task_id, errmsg):
    """
    更新task的异常信息
    :param task_id:
    :param errmsg:
    :return:
    """
    db.testtasks.update_one({'_id': ObjectId(task_id)}, {'error': errmsg})


def get_config_by_project(project_id):
    """
    获取项目的配置参数
    :param project_id:
    :return:
    """

    if not project_id:
        return None

    return db.envs.find_one({'projectId': project_id, 'env': DEFAULT_ENV})

def get_config_by_task(task_id):

    task = db.tasks.find_one({'_id': ObjectId(task_id)}, {'projectId': 1})
    project_id = task.get('projectId')
    return get_config_by_project(project_id)

def get_sql_by_project(project_id):
    """
    获取项目的sql脚本
    :param project_id:
    :return:
    """
    if not project_id:
        return None

    return db.sqls.find_one({'projectId': project_id, 'env': DEFAULT_ENV})


def exec_sql(sql, host, port, user, password):
    """
    执行sql脚本
    :param sql:
    :param conn_options: 连接参数
    :return:
    """
    if not sql:
        return
    with SimpleMysql(host=host, port=port, user=user, passwd=password) as conn:
        conn.execute(sql)
