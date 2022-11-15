# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import AsyncDaoModel, DaoModel
from connect import connect_db, redis_cluster, asyncio_mongo

__models__ = ['BackgroundJobsModel']

BackgroundJobsModel = DaoModel(connect_db.db.background_jobs, redis=redis_cluster, broker=Config.BROKER_URL,
                        project=Config.PROJECT)
