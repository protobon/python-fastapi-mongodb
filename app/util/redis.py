from app.common.config import Config


def get_redis_client():
    return Config().redis_client()
