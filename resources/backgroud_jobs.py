# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource

from connect import security
from constants import Constants
from enums.background_jobs import BackgroundJobsType
from helper.background_jobs import BackgroundJobsHelper
from schemas.background_jobs import BackgroundJobsSchema
import pydash as py_

class BackgroundJobsResource(Resource):

    @security.http(
        login_required=False,
        form_data=BackgroundJobsSchema()
    )
    def post(self, form_data):
        # NOTE: each type NFT and BOX will have 2 log, 1 for mint from contract, 1 for mint from BE
        BackgroundJobsHelper.add(form_data=form_data)

        form_data['type'] = BackgroundJobsType.REFERRAL_COMMISSION
        BackgroundJobsHelper.add(form_data=form_data)
        return {}
