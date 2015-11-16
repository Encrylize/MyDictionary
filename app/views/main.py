from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
@login_required
def index():
    return "Logged in"


@main.route("/login")
def login():
    return render_template("login.html")