from flask import Blueprint, render_template, url_for, request, session, redirect
from flask_login import login_required, login_user, current_user
from flask_oauthlib.client import OAuthException

from app import db
from app.models import User
from app.oauth import facebook

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/index")
@login_required
def index():
    return "Logged in"


@views.route("/login")
def login():
    return render_template("login.html")


@views.route("/authorize")
def authorize():
    return facebook.authorize(url_for("views.callback", _external=True))


@views.route("/callback")
def callback():
    resp = facebook.authorized_response()
    if resp is None:
        return "Access denied: Reason: %s, error: %s" % (
            request.args["error_reason"], request.args["error_description"]
        )
    elif isinstance(resp, OAuthException):
        return "Access denied: %s" % resp.message

    session["oauth_token"] = (resp["access_token"], "")
    me = facebook.get("/me")

    user = User.query.filter_by(social_id=me.data.get("id")).first()
    if user is None:
        user = User(social_id=me.data.get("id"), name=me.data.get("name"))
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for("views.index"))