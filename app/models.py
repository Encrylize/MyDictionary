from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    dictionary = db.relationship("Dictionary", backref="creator", uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        """ Initializes the user and creates their dictionary. """
        super().__init__(**kwargs)
        self.dictionary = Dictionary(creator=self)

    def __repr__(self):
        return "<User ID: %r, social_id: %r, name: %r>" % (self.id, self.social_id, self.name)


class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Dictionary ID: %d, user_id: %d>" % (self.id, self.user_id)