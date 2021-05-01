import os
import pymongo
from typing import Dict, Optional, Any


class Mongo:
    def __init__(self,
                 db: Optional[str] = None,
                 coll: Optional[str] = None,
                 *args,
                 **kwargs):
        self._client = pymongo.MongoClient(os.getenv("MONGO_HOST"))
        if db is not None:
            self._db = self._client[db]
        if coll is not None:
            self._coll = self._db[coll]

    def _find(self, query: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if query:
            return self._coll.find_one(query)
        return self._coll.find()

    def _update(self,
                query: Dict[str, Any],
                data: Dict[str, Dict[str, Any]],
                upsert: bool = True) -> None:
        Mongo._coll.update_one(query, data, upsert=upsert)

    def _delete(self, query: Dict[str, Any]) -> None:
        Mongo._coll.delete_one(query)


Mongo.init()