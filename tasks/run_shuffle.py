

from worker import worker
import pydash as py_
import sentry_sdk
import traceback
from pymongo import MongoClient
from config import Config
import random
from lib.utils import dt_utcnow

db = MongoClient(Config.MONGO_URI, connect=False)['katana-dapp']
CollectionModel = db['collection']
ShuffledCollectionModel = db['shuffled_collection']

@worker.task(name='worker.run_shuffle', rate_limit='100/s')
def run_shuffle(collection_address: str):
    try:
        _collection = CollectionModel.find_one(filter={
            'address': collection_address.lower()    
        })
        _is_box = py_.get(_collection, 'is_box', False)
        if _is_box:
            _total_supply = py_.get(_collection, 'total_supply', 0)
            if _total_supply:
                _types_list =py_.get(_collection, 'types_list')
                _collection_indexes = []
                for _idx, _type in enumerate(_types_list):
                    _weight_per_type = int(_total_supply * (py_.get(_type, 'rate')) / 100.0)
                    for i in range(_weight_per_type):
                        _collection_indexes.append(_idx)
                if len(_collection_indexes) < _total_supply:
                    _lost = _total_supply - len(_collection_indexes)
                    _collection_indexes += [_collection_indexes[0] for i in range(_lost)]
    
                random.shuffle(_collection_indexes)
                random.shuffle(_collection_indexes)
                random.shuffle(_collection_indexes)

                ShuffledCollectionModel.insert_one({
                    'contract': collection_address.lower(),
                    'shuffled_indexes': _collection_indexes,
                    'created_time': dt_utcnow(),
                    'created_by': 'smc-jobs-iapi-worker'
                })
        return f"DONE - shuffle for cntract: {collection_address}"
    except:
        traceback.print_exc()
        sentry_sdk.capture_exception()
        return f"FAIL - shuffle for contract: {collection_address}"