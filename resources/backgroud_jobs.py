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
from tasks import run_shuffle

class BackgroundJobsResource(Resource):

    @security.http(
        login_required=False,
        form_data=BackgroundJobsSchema()
    )
    def post(self, form_data):
        """
            Run shuffle for all token Ids in the collection in the beginning of collection creation
        """
        _contract = py_.get(form_data, 'contract')
        run_shuffle.delay(_contract)

        # NOTE: each type NFT and BOX will have 2 log, 1 for mint from contract, 1 for mint from BE
        BackgroundJobsHelper.add(form_data=form_data)

        if form_data['type'] == BackgroundJobsType.NFT:
            form_data['type'] = BackgroundJobsType.REFERRAL_COMMISSION
        elif form_data['type'] == BackgroundJobsType.BOX:
            form_data['type'] = BackgroundJobsType.BOX_REFERRAL_COMMISSION
            
        BackgroundJobsHelper.add(form_data=form_data)
        return {}
