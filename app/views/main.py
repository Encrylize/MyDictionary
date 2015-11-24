from flask import Blueprint, render_template, g, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user, logout_user
from sqlalchemy_utils import get_class_by_table

from app import db
from app.models import Word
from app.utils import get_or_create
from app.forms import SearchForm

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/index")
@main.route("/index/<int:page>")
@login_required
def index(page=1):
    words = g.user.dictionary.words.paginate(page, current_app.config.get("WORDS_PER_PAGE"), False)
    if not words.items and page != 1:
        abort(404)

    return render_template("index.html", title="Home", words=words)


@main.route("/new/<word_class:word_class>", methods=["GET", "POST"])
@login_required
def create_word(word_class):
    form = word_class.form()

    if form.validate_on_submit():
        word, created = get_or_create(word_class, dictionary=g.user.dictionary,
                                      **{key: value for key, value in form.data.items() if key != "next"})
        if created:
            db.session.add(word)
            db.session.commit()
            flash("Successfully created word!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("An identical word already exists.", "error")

    return render_template("form.html", title="New Word", form=form)


@main.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_word(id):
    word = Word.query.filter_by(id=id, dictionary=g.user.dictionary).first_or_404()
    form = word.form(obj=word)

    if form.validate_on_submit():
        new_word = get_class_by_table(Word, Word.__table__, data={"type": word.type}).query.filter_by(
           **{key: value for key, value in form.data.items() if key != "next"}).first()
        if new_word is None:
            form.populate_obj(word)
            db.session.commit()
            flash("Successfully edited word!", "success")
            return form.redirect("index")
        else:
            flash("An identical word already exists.", "error")

    return render_template("form.html", title="Edit Word", form=form)


@main.route("/delete/<int:id>")
@login_required
def delete_word(id):
    word = Word.query.filter_by(id=id, dictionary=g.user.dictionary).first_or_404()
    db.session.delete(word)
    db.session.commit()
    flash("Deleted word.", "warning")

    return redirect(url_for("main.index"))


@main.route("/search", methods=["POST"])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for("main.index"))
    return redirect(url_for("main.search_results", query=g.search_form.search_field.data))


@main.route("/search_results/<query>")
@main.route("/search_results/<query>/<int:page>")
@login_required
def search_results(query, page=1):
    words = None
    return render_template("search_results.html", title="Search Results", query=query, words=words)


@main.route("/login")
def login():
    if g.user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("login.html", title="Log In")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.before_request
def before_request():
    g.user = current_user
    g.word_classes = [word_class.__mapper_args__["polymorphic_identity"] for word_class in Word.__subclasses__()]
    g.search_form = SearchForm()