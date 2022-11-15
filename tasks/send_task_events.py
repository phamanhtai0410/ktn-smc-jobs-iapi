# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import os
import subprocess

import pydash as py_
import sentry_sdk

from logger import debug
from worker import worker
from bson import json_util
from enums.background_jobs import BackgroundJobsType
from config import Config

_dict = os.getcwd()

@worker.task(name='worker.send_task_events', rate_limit='1000/s')
def send_task_events(event):
    debug('# Send task for handle event: ', event)
    _event = json_util.loads(event)
    _event_name = py_.get(_event, 'event')
    _contract = py_.get(_event, 'address')
    _event_type = py_.get(_event, 'event_type')

    _task_name = py_.get(Config.SEND_TASKS_NAME, f'{_event_type}.{_event_name}')

    if not _task_name:
        sentry_sdk.capture_message(f'FAIL - not config handle for: {_contract}, {_event}, {_event_type}')
        return f'FAIL - not config handle for: {_contract}, {_event}, {_event_type}'

    print('# task_name', _task_name)

    worker.send_task(_task_name, (json_util.dumps(_event), ))

    return f'DONE - send_task {_task_name} for: {_contract}, {_event}, {_event_type}'