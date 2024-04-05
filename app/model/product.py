from mongoengine import (DynamicDocument, StringField, DateTimeField, IntField)


class Product(DynamicDocument):
    meta = {
        'collection': 'product',
        'db_alias': 'warehouseDB'
    }

    title = StringField(required=True, min_length=2, max_length=125)
    quantity = IntField(required=True, default=0, min_value=0, max_value=10000000)
    createdAt = DateTimeField(required=True)
