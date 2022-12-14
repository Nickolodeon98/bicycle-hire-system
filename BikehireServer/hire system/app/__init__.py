from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_mail import Mail


import redis
import logging
from logging.handlers import RotatingFileHandler
from app.utils.commons import ReConverter

#datebase
db = SQLAlchemy()

# create redis object
redis_store = None

#flask_mail
mail = Mail()
# logging

logging.basicConfig(level=logging.INFO)
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)




def create_app(config_name):
    """
    create flask app object
    :param config_name: str name of config model("develop","product")
    :return:
    """
    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    mail.init_app(app)
    db.init_app(app)
    # init redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # use flask-session save session into redis
    Session(app)
    # CSRFProtect(app)

    from . import api_1
    app.register_blueprint(api_1.api, url_prefix="/api/v1.0")
    # add converter into app object
    app.url_map.converters["re"] = ReConverter

    from app import web_html
    app.register_blueprint(web_html.html)
    return app

