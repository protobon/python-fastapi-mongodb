from mongoengine import connect


class MongoEngine:
    def __init__(self, uri: str, alias: str):
        connect(host=uri, alias=alias)
