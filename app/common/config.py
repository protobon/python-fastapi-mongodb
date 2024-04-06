import yaml
from app.common.constants import Constants
from app.db.mongodb import MongoEngine
from redis import StrictRedis
from singleton_decorator import singleton


@singleton
class Config:
    config = dict()
    mongo = dict()
    redis = dict()

    def __init__(self, path: str):
        if path:
            with open(path) as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        if self.config:
            if self.config.get(Constants.MONGODB.main):
                with open(self.config[Constants.MONGODB.main]) as f:
                    self.mongo = yaml.load(f, Loader=yaml.FullLoader)
                if self.mongo:
                    self.load_mongodb(self,
                                      uri=self.mongo[Constants.MONGODB.uri],
                                      alias=self.mongo[Constants.MONGODB.alias])
            if self.config.get(Constants.REDIS.main):
                with open(self.config[Constants.REDIS.main]) as f:
                    self.redis = yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def load_mongodb(self, uri: str, alias: str):
        MongoEngine(uri=uri, alias=alias)

    def redis_client(self):
        return StrictRedis(host=self.redis["host"], port=int(self.redis["port"]), decode_responses=True)
