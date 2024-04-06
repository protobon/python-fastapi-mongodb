import orjson
from redis import StrictRedis
from typing import Optional, List

from app.util.mongodb import MongoCursorParser


class Cache:
    def __init__(self,
                 client: StrictRedis,
                 collection,
                 name: str,
                 pipeline: Optional[List[dict]],
                 refresh_in_seconds: int):
        self.client = client
        cursor = collection.objects().aggregate(pipeline, allowDiskUse=True)
        for document in cursor:
            doc = MongoCursorParser.remove_oid(document)
            client.setex(name=f"{name}:{doc['_id']}", time=refresh_in_seconds, value=orjson.dumps(doc))
        client.setex(f"{name}__alive", time=refresh_in_seconds, value=1)  # flag

    def get_all(self, name: str) -> List[dict]:
        all_items = [key for key in self.client.scan_iter(f"{name}:*")]
        return [orjson.loads(self.client.get(key)) for key in all_items]

    def get_by_id(self, item_id: str):
        return orjson.loads(self.client.get(item_id))
