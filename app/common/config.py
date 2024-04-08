from app.common.constants import EnvConstants as Env
from mongoengine import connect
from redis import StrictRedis
from singleton_decorator import singleton
import os


@singleton
class Config:
    mongo = dict()
    redis = dict()

    def __init__(self):
        if not self.mongo:
            self.mongo[Env.MONGODB.uri] = os.getenv(Env.MONGODB.uri)
            self.mongo[Env.MONGODB.alias] = os.getenv(Env.MONGODB.alias)
            if len(self.mongo) == 2:
                self.load_mongodb()

        if not self.redis:
            self.redis[Env.REDIS.host] = os.getenv(Env.REDIS.host)
            self.redis[Env.REDIS.port] = int(os.getenv(Env.REDIS.port))
            self.redis[Env.REDIS.password] = os.getenv(Env.REDIS.password)

    def load_mongodb(self):
        connect(host=self.mongo[Env.MONGODB.uri], alias=self.mongo[Env.MONGODB.alias])

    def redis_client(self):
        return StrictRedis(host=self.redis[Env.REDIS.host],
                           port=self.redis[Env.REDIS.port],
                           password=self.redis[Env.REDIS.password],
                           decode_responses=True)
