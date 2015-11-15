from flask import Blueprint
from flask_login import login_required

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/index")
@login_required
def index():
    return "Logged in"