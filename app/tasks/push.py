# -*- coding: utf-8 -*-
import logging
from app.application import app
from app.tasks.base import BaseTask

logger = logging.getLogger(__name__)

@app.task(base=BaseTask, bind=True, soft_time_limit=10, name='push.push_message_to_user')
def push_message_to_user(self, userID, message, action_type):
    str ='userID: %s, message: %s, action_type: %s' % (userID, message, action_type)
    logger.info(str)
