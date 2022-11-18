# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sentry_sdk
from celery import Celery
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from config import Config
from connect import connect_db
from celery.signals import worker_ready


def create_worker():
    app = Flask(__name__)
    connect_db.init_app(app, Config.MONGO_URI)
    _celery = Celery(__name__, broker=Config.BROKER_URL)
    _celery.conf.update(Config.__dict__)

    if Config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=Config.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            debug=True,
            server_name=f'worker_{Config.PROJECT}'
        )

    return _celery


# init connect db


worker = create_worker()

from helper.background_jobs import BackgroundJobsHelper

@worker_ready.connect()
def message_poll_start(sender=None, headers=None, body=None, **kwargs):
    print('-'*10, 'WORKER START', '-'*10)
    BackgroundJobsHelper.restart()
    print('-'*10, 'DONE RESTART WORKER', '-'*10)