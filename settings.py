# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
