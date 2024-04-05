import yaml
from app.common.constants import Constants
from app.db.mongodb import MongoEngine


class Config:
    config = dict()
    mongo = dict()

    @classmethod
    def init(cls, path: str):
        if path:
            with open(path) as f:
                cls.config = yaml.load(f, Loader=yaml.FullLoader)
        if cls.config:
            if cls.config.get(Constants.MONGODB.main):
                with open(cls.config[Constants.MONGODB.main]) as f:
                    cls.mongo = yaml.load(f, Loader=yaml.FullLoader)
                if cls.mongo:
                    cls.load_mongodb(uri=cls.mongo["uri"], alias=cls.mongo["alias"])

    @classmethod
    def load_mongodb(cls, uri: str, alias: str):
        MongoEngine(uri=uri, alias=alias)
