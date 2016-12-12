# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-12.
  以接口为单位的测试队列
"""

from app import app

@app.task
def add_api(x, y):

    print x, y

