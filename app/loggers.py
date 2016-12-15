# -*- coding: utf-8 -*-
"""
    for description
"""

import logging

from raven.handlers.logging import SentryHandler
from raven import Client, setup_logging

from configs import log_level, log_handler, sentry_dsn

def init_logging():
    _level = 'INFO' if log_level is None else log_level
    _handlers = 'console' if log_handler is None else log_handler

    _simple_fmt = logging.Formatter('%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d] %(message)s')

    _logger = logging.root
    _logger.setLevel(_level)

    _handlers = _handlers.split(',')

    if 'console' in _handlers:
        _console_handler = logging.StreamHandler()
        _console_handler.setFormatter(_simple_fmt)
        _console_handler.setLevel(_level)
        _logger.addHandler(_console_handler)

    if 'sentry' in _handlers:
        if sentry_dsn is not None and sentry_dsn != '':

            client = Client(dsn=sentry_dsn, level=_level)
            _sentry_handler = SentryHandler(client)
            setup_logging(_sentry_handler)
