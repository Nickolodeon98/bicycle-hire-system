import redis

class Config(object):
    DEBUG = True
    use_reloader = False
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"
    #DATEBASE
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///system.db'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/bike"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #flask-session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400 #In seconds

    #flask mail
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "729823753@qq.com"
    MAIL_PASSWORD = 'vurepnqklsymbcce'
    MAIL_DEFAULT_SENDER = "729823753@qq.com"

class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}

#email address of sender

# MAIL_SERVER = "smtp.gmail.com"
# MAIL_PORT = 465
# MAIL_USE_SSL = True

# MAIL_SERVER="smtp.gmail.com"
# MAIL_PROT='587'
# MAIL_USE_TLS=True
# MAIL_USERNAME = 'jikaisong1997@gmail.com'
# # MAIL_PASSWORD = 'bjuptolgisabncup'
# MAIL_PASSWORD = 'ao281072594'
# MAIL_DEFAULT_SENDER = 'jikaisong1997@gmail.com'
