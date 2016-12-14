# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-13.
  summary
"""
from pymongo import MongoClient

from configs import mongo_uri

print mongo_uri

_client = MongoClient(mongo_uri)
db = _client.get_default_database()
