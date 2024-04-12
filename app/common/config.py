import firebase_admin
from firebase_admin import credentials
from mongoengine import connect
from redis import StrictRedis
from singleton_decorator import singleton
from os import getenv

from app.common.constants import EnvConstants as Env


@singleton
class Config:
    app = dict()
    mongo = dict()
    redis = dict()
    firebase_app = None

    def __init__(self):
        if not self.app:
            self.app[Env.APP.name] = getenv(Env.APP.name)
            self.app[Env.APP.host] = getenv(Env.APP.host)
            self.app[Env.APP.port] = int(getenv(Env.APP.port))
        if not self.mongo:
            self.mongo[Env.MONGODB.uri] = getenv(Env.MONGODB.uri)
            self.mongo[Env.MONGODB.alias] = getenv(Env.MONGODB.alias)
            if len(self.mongo) == 2:
                self.load_mongodb()

        if not self.redis:
            self.redis[Env.REDIS.host] = getenv(Env.REDIS.host)
            self.redis[Env.REDIS.port] = int(getenv(Env.REDIS.port))
            self.redis[Env.REDIS.password] = getenv(Env.REDIS.password)

        if not self.firebase_app:
            cred = credentials.Certificate(getenv(Env.FIREBASE.config))
            self.firebase_app = firebase_admin.initialize_app(cred)

    def load_mongodb(self):
        connect(host=self.mongo[Env.MONGODB.uri], alias=self.mongo[Env.MONGODB.alias])

    def redis_client(self):
        return StrictRedis(host=self.redis[Env.REDIS.host],
                           port=self.redis[Env.REDIS.port],
                           password=self.redis[Env.REDIS.password],
                           decode_responses=True)
