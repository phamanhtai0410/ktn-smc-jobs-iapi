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


class HealthCheck(Resource):

    @security.http(
        login_required=False
    )
    def get(self, *args, **kwargs):
        
        return {}
