import redis

class Config(object):
    DEBUG = True
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"
    #DATEBASE
    SQLALCHEMY_DATABASE_URI = 'sqlite:///system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #flask-session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400 #In seconds

class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}