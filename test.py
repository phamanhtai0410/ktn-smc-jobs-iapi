# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sys

from pydash import get
from pymongo import MongoClient

sys.path.append(".")
from rediscluster import RedisCluster

from config import Config

redis_cluster = RedisCluster(
    startup_nodes=Config.REDIS_CLUSTER,
    decode_responses=True,
    skip_full_coverage_check=True
)

db = MongoClient(Config.MONGO_URI, connect=False)['katana-dapp']


class PointDao():
    def __init__(self, *args, **kwargs):
        self.redis = redis_cluster

    def key_of_event(self, event):
        return f'ktn:points:events:{event}'

    def get_rank(self, event, page, page_size):
        if page <= 0:
            page = 1
        _start = (page - 1) * page_size
        _end = page * page_size
        _rank = self.redis.zrevrange(self.key_of_event(event), _start, _end - 1, withscores=True)
        return [{
            'rank': _start + _ind + 1,
            'point': val[1],
            'address': val[0]
        } for _ind, val in enumerate(_rank)], self.redis.zcard(self.key_of_event(event))

    def set_rank(self, event, address, point):
        self.redis.zadd(self.key_of_event(event), {address: point})

    def get_rank_of(self, event, address):
        _rank = self.redis.zrevrank(self.key_of_event(event), address)
        if not isinstance(_rank, (int, float)):
            return -1
        return _rank + 1



pointModel = PointDao()

points = db.points.find({})
# for _point in points:
#     pointModel.set_rank(event=get(_point, 'event'),point=get(_point, 'total_points'),address=get(_point, 'address'))
print(pointModel.get_rank(event='top_referral', page=1, page_size=2))
print(pointModel.get_rank_of(event='stake', address="0x29e754233f6a50ee5ae3ee6a0217ad907dc3386b"))
