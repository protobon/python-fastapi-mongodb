from redis import StrictRedis
from app.common.config import Config


def get_redis_client() -> StrictRedis:
    return Config().redis_client()
