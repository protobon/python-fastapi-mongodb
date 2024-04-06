from bson import json_util
import re
from typing import Iterable, List


class MongoCursorParser:
    _id_: str = 'custom_serializer'
    result: str = _id_ + "_result_"
    error: str = _id_ + "_error_"

    @classmethod
    def remove_oid(cls, obj: dict) -> dict:
        obj_str = json_util.dumps(obj)
        while True:
            pattern = re.compile('{\s*"\$oid":\s*(\"[a-z0-9]{1,}\")\s*}')
            match = re.search(pattern, obj_str)
            if match:
                obj_str = obj_str.replace(match.group(0), match.group(1))
            else:
                return json_util.loads(obj_str)

    @classmethod
    def parse(cls, list_obj: Iterable) -> List[dict]:
        objects_out = []
        for obj in list_obj:
            objects_out.append(cls.remove_oid(obj))
        return objects_out
