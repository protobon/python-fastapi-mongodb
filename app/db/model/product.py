from datetime import datetime
from marshmallow import Schema, fields


class ProductSchema(Schema):
    title: str = fields.Str()
    createdAt: datetime = fields.DateTime()
    quantity: int = fields.Int()
