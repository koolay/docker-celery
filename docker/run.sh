#!/bin/sh

celery -A $APP_NAME worker --loglevel=$LOG_LEVEL --concurrency=$CONCURRENCY -n worker@%h
