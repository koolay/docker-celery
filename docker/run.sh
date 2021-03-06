#!/bin/sh

celery -A $APP_NAME flower --port=5555 & celery -A $APP_NAME worker --loglevel=$LOG_LEVEL --concurrency=$CONCURRENCY -n worker@%h
