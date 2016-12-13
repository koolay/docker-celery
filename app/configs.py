# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""
import os

redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
redis_db = int(os.environ.get('REDIS_DB'))
redis_password = os.environ.get('REDIS_PASSWORD')

if redis_password:
    redis_uri = 'redis://:{3}@{0}:{1}/{2}'.format(redis_host, redis_port, redis_db, redis_password)
else:
    redis_uri = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)

mongo_uri = os.environ.get('MONGO_URI')
