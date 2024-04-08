class MongoDB:
    alias = "MONGODB_ALIAS"
    uri = "MONGODB_URI"


class Redis:
    host = "REDIS_HOST"
    port = "REDIS_PORT"
    password = "REDIS_PASSWORD"


class EnvConstants:
    MONGODB = MongoDB()
    REDIS = Redis()
