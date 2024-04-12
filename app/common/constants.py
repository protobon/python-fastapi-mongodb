class App:
    name = "APP_NAME"
    host = "APP_HOST"
    port = "APP_PORT"


class MongoDB:
    alias = "MONGODB_ALIAS"
    uri = "MONGODB_URI"


class Redis:
    host = "REDIS_HOST"
    port = "REDIS_PORT"
    password = "REDIS_PASSWORD"


class Firebase:
    config = "FIREBASE_CONFIG"


class EnvConstants:
    APP = App()
    MONGODB = MongoDB()
    REDIS = Redis()
    FIREBASE = Firebase()
