import os
import pymongo
from typing import Dict, Optional, Any


class Mongo(object):
    client: pymongo.MongoClient = None

    @staticmethod
    def init() -> None:
        Mongo.client = pymongo.MongoClient(os.getenv("MONGO_HOST"))

    @staticmethod
    def find(db: str,
             coll: str,
             query: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if query:
            return Mongo.client[db][coll].find_one(query)
        return Mongo.client[db][coll].find()

    @staticmethod
    def update(db: str,
               coll: str,
               query: Dict[str, Any],
               data: Dict[str, Dict[str, Any]],
               upsert: bool = True) -> None:
        Mongo.client[db][coll].update_one(query, data, upsert=upsert)

    @staticmethod
    def delete(db: str, coll: str, query: Dict[str, Any]) -> None:
        Mongo.client[db][coll].delete_one(query)


Mongo.init()