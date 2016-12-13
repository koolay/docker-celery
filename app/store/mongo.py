# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""
from pymongo import MongoClient

from configs import mongo_uri

_client = MongoClient(mongo_uri)
_dbname = _client.get_default_database()
db = _client[_dbname]