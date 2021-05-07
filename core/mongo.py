import os
import pymongo
from typing import Dict, Optional, Any

__all__ = ('Mongo', )


class Mongo:
    def __init__(self, db: str, coll: str, *args, **kwargs) -> None:
        self._client = pymongo.MongoClient(os.getenv("MONGO_HOST"))
        self._db = self._client[db]
        self._coll = self._db[coll]

    def find(self, query: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if query:
            return self._coll.find_one(query)
        return self._coll.find()

    def update(self,
               query: Dict[str, Any],
               data: Dict[str, Dict[str, Any]],
               upsert: bool = True) -> None:
        self._coll.update_one(query, data, upsert=upsert)

    def delete(self, query: Dict[str, Any]) -> None:
        self._coll.delete_one(query)
