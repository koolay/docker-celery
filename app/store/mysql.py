# -*- coding: utf-8 -*-
"""
  Created by koolay on 16-12-14.
  summary
"""
import json

import pymysql.cursors
import logging

logger = logging.getLogger(__name__)


class SimpleMysql:
    conn = None
    cur = None

    def __init__(self, **kwargs):
        """ construct """
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 3306)
        self.db = kwargs.get("db", None)
        self.user = kwargs.get('user')
        self.passwd = kwargs.get('passwd')

        self.keep_alive = kwargs.get("keep_alive", False)
        self.charset = kwargs.get("charset", "utf8")
        self.autocommit = kwargs.get("autocommit", False)
        self.connect_timeout = kwargs.get('connect_timeout', 3)

        self._check_args()
        self.connect()

    def _check_args(self):
        """ check args of structure"""
        if self.host is None or self.user is None or self.passwd is None:
            raise Exception('db参数配置不完整')

    def connect(self):
        """Connect to the mysql server"""

        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.passwd,
                                        db=self.db,
                                        charset=self.charset,
                                        cursorclass=pymysql.cursors.DictCursor,
                                        connect_timeout=self.connect_timeout)

            self.cur = self.conn.cursor()
            self.conn.autocommit(self.autocommit)
        except:
            logger.error("MySQL connection failed, host: %s" % self.host)
            raise

    def execute(self, sql, params=None):
        """
        check if connection is alive. if not, reconnect
        :param sql:
        :param params:
        :rtype Cursor:
        """

        self.cur.execute(sql, params)
        return self.commit()

    def commit(self):
        """Commit a transaction (transactional engines like InnoDB require this)"""
        return self.conn.commit()

    def is_open(self):
        """Check if the connection is open"""
        return self.conn.open

    def end(self):
        """Kill the connection"""
        self.cur.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()
