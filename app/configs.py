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
log_level = os.environ.get('LOG_LEVEL')
log_handler = os.environ.get('LOG_HANDLER')
sentry_dsn = os.environ.get('SENTRY_DSN')