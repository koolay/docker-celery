# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-12.
　以项目为单位的测试队列
"""
from app import app
from tasks.task import TestingTask

@app.task(base=TestingTask)
def add(x, y):
    return x + y

