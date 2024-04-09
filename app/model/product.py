from bson.objectid import ObjectId
from mongoengine import (DynamicDocument, StringField, DateTimeField, IntField)
from app.common.constants import EnvConstants as Env
from app.util.mongodb import MongoCursorParser
from typing import List
from os import getenv


class Product(DynamicDocument):
    meta = {
        'collection': 'product',
        'db_alias': getenv(Env.MONGODB.alias)
    }

    title = StringField(required=True, min_length=2, max_length=125)
    quantity = IntField(required=True, default=0, min_value=0, max_value=10000000)
    createdAt = DateTimeField(required=True)


def get_products_by_filter(fields: dict) -> List[dict]:
    pipeline = [
        {
            "$match": fields
        }
    ]
    cursor = Product.objects().aggregate(pipeline, allowDiskUse=True)
    return MongoCursorParser.parse(cursor)


def get_product_by_id(product_id: str) -> Product:
    return Product.objects(_id=ObjectId(product_id)).first()
