# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate

from enums.background_jobs import BackgroundJobsType


class BackgroundJobsSchema(Schema):
    class Meta:
        unknown = RAISE

    contract = fields.String(required=True, allow_none=False)
    type = fields.String(required=True, validate=validate.OneOf([BackgroundJobsType.NFT, BackgroundJobsType.BOX]), allow_none=False)
    from_block = fields.Int(required=True, allow_none=False)