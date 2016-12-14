# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""
import os

redis_uri = os.environ.get('REDIS_URI')
mongo_uri = os.environ.get('MONGO_URI')
http_timeout = os.environ.get('HTTP_TIMEOUT')
http_timeout = 5 if not http_timeout else int(http_timeout)