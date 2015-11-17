from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required, current_user, logout_user

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
@login_required
def index():
    return render_template("index.html")


@main.route("/login")
def login():
    if g.user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.before_request
def before_request():
    g.user = current_user