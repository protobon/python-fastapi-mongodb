from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class CustomBaseModel(BaseModel):

    def dict(self, *args, **kwargs):
        result = self.__dict__

        for key, value in result.items():
            if isinstance(value, FieldInfo):
                result[key] = value.default
            if isinstance(value, CustomBaseModel):
                result[key] = value.dict()
            elif isinstance(value, datetime):
                result[key] = value.__str__()
            elif isinstance(value, list) and all(isinstance(item, CustomBaseModel) for item in value):
                result[key] = [item.dict() for item in value]

        return result


class Header(CustomBaseModel):
    transactionId: str
    user: Optional[str]
    uid: Optional[str]
    pageSize: int = 0
    pageNumber: int = 0


class Body(CustomBaseModel):
    result: bool
    error: str
    timestamp: str
    message: str
    data: dict


class Response(CustomBaseModel):
    header: Header
    body: Body
