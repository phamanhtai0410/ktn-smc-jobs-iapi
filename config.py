# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    PROJECT = "dapp-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')
    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')

    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    # Config celery worker

    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.on_transfer_nft': {'queue': 'ktn-nft-queue'},
        'worker.on_token_created': {'queue': 'ktn-nft-queue'},
        'worker.on_mint_order_from_dev': {'queue': 'ktn-referral-commission-queue'},
        'worker.on_mint_order_from_dapp_creator': {'queue': 'ktn-referral-commission-queue'},
        'worker.send_task_events': {'queue': 'ktn-smc-jobs-iapi-queue'},
        'worker.run_background_jobs': {'queue': 'ktn-smc-jobs-iapi-queue'},
        'worker.on_created_box': {'queue': 'ktn-nft-queue'},
        'worker.on_transfer_box': {'queue': 'ktn-nft-queue'},
        'worker.on_open_box': {'queue': 'ktn-nft-queue'},
    }

    SEND_TASKS_NAME = {
        'NFT': {
            'Transfer': 'worker.on_transfer_nft',
            'TokenCreated': 'worker.on_token_created',
            'MintFromBoxOpening': 'worker.on_mint_from_box'

        },
        'REFERRAL_COMMISSION': {
            'MintOrderForDev': 'worker.on_mint_order_from_dev',
            'MintOrderFromDaapCreator': 'worker.on_mint_order_from_dapp_creator',

        },
        'BOX': {
            'TokenCreated': 'worker.on_created_box',
            'SendNft': 'worker.on_transfer_box',
            'OpenBox': 'worker.on_open_box',
        },
        'BOX_REFERRAL_COMMISSION': {
            'MintOrderForDev': 'worker.on_mint_order_from_dev',
            'MintOrderFromDaapCreator': 'worker.on_mint_order_from_dapp_creator',

        },
    }

    ABIS_PATH =  {
        'NFT': 'abis/katana_nft.json',
        'REFERRAL_COMMISSION': 'abis/katana_nft.json',
        'BOX': 'abis/katana_box.json',
        'BOX_REFERRAL_COMMISSION': 'abis/katana_box.json',

    }

    PUBLIC_PATH = os.getenv('PUBLIC_PATH')
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))

    RPC_URIS = json.loads(os.getenv('RPC_URIS', default='[]'))

    API_URL = os.getenv('API_URL', 'http://localhost:5005')
