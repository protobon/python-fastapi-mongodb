from mongoengine import connect


class MongoEngine:
    def __init__(self, uri: str, alias: str):
        self.client = connect(host=uri, alias=alias)

    def get_session(self):
        return self.client
