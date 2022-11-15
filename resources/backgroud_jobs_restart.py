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

class BackgroundJobsRestartResource(Resource):

    @security.http(
        login_required=False,
    )
    def post(self):
        BackgroundJobsHelper.restart()
        return {}

    
