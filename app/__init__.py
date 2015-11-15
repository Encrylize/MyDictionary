from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.client import OAuth

from config import config

db = SQLAlchemy()
lm = LoginManager()
oauth = OAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    lm.init_app(app)
    oauth.init_app(app)

    from app.views import views
    app.register_blueprint(views)

    return app