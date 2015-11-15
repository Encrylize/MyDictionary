from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String())

    def __repr__(self):
        return "<User ID: %r, social_id: %r, name: %r, email: %r>" % (self.id, self.social_id, self.name, self.email)