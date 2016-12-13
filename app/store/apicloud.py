# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""

from store.mongo import db


def get_testCase_by_project(project_id):
    """
    根据项目id获取项目下的所有测试用例
    :param project_id:
    :return:
    """

    if not project_id:
        return []

    items = []

    for path in db.paths.find({'projectId': project_id}, {'_id': 1}):
        print 'get path by id:' + str(path['_id'])
        for mock in db.mocks.find({'pathId': str(path['_id'])}):
            print 'found:' + str(mock['_id'])
            items.append(mock)

    return items
