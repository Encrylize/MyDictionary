from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.client import OAuth

from config import config

db = SQLAlchemy()
oa = OAuth()
lm = LoginManager()
lm.login_view = "views.login"

from app.models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    lm.init_app(app)
    oa.init_app(app)

    from app.views import views
    from app.views.oauth import oauth
    app.register_blueprint(views)
    app.register_blueprint(oauth)

    return app