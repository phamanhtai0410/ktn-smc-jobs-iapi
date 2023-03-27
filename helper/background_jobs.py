# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from eth_account.messages import defunct_hash_message
from pymongo import ReturnDocument
from config import Config

from lib.utils import dt_utcnow, util_web3

from models import BackgroundJobsModel
from tasks import run_background_job

from bson import json_util
from bson.objectid import ObjectId

import pydash as py_

class BackgroundJobsHelper:
    '''
    '''

    @classmethod
    def add(cls, form_data: dict):
        _type = py_.get(form_data, 'type')
        _abi_path = py_.get(Config.ABIS_PATH, _type)
        if not _abi_path:
            raise Exception('Not found abis_path')
            
        _job = BackgroundJobsModel.col.find_one_and_update(
            filter={
                'contract': form_data['contract'].lower(),
                'type': _type,
        }, update={
            '$set': {
                'abi_path': _abi_path,
                'from_block': form_data['from_block'],
                'chain': py_.get(form_data, 'chain')
            }
        }, upsert=True, return_document=ReturnDocument.AFTER)

        if not _job.get('active'):
            return cls.start(_job)
        return _job['task_id']

    @classmethod
    def start(cls, job):
        _task = run_background_job.delay(
            json_util.dumps(job)
        )
        _job = BackgroundJobsModel.update_one(
            filter={
                '_id': job['_id'] if isinstance(job['_id'], ObjectId) else ObjectId(job['_id'])
            },
            obj={
                'task_id': str(_task),
                'active': True,
                'updated_by': 'api'
            }
        )
        return str(_task)

    @classmethod
    def restart(cls):
        _jobs = BackgroundJobsModel.find({})
        _tasks = []
        for _job in _jobs:
            _task = cls.start(_job)
            _tasks.append(_task)
        return _tasks
    
