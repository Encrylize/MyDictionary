from flask_login import UserMixin

from app import db
from app.forms import WordForm, NounForm, VerbForm, AdjectiveForm, AdverbForm, ConjunctionForm, PrepositionForm


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
    words = db.relationship("Word", backref="dictionary", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Dictionary ID: %d, user_id: %d>" % (self.id, self.user_id)


class Word(db.Model):
    # General
    id = db.Column(db.Integer, primary_key=True)
    form = WordForm
    meaning = db.Column(db.String())
    examples = db.Column(db.String())
    type = db.Column(db.String())
    dictionary_id = db.Column(db.Integer, db.ForeignKey("dictionary.id"))

    # Noun
    singular = db.Column(db.String())
    plural = db.Column(db.String())
    gender = db.Column(db.String())

    # Verb
    infinitive = db.Column(db.String())
    past_tense = db.Column(db.String())
    present_perfect_tense = db.Column(db.String())
    consonant_change = db.Column(db.Boolean())

    # Adjective
    positive = db.Column(db.String())
    comparative = db.Column(db.String())
    superlative = db.Column(db.String())

    # Adverb
    adverb = db.Column(db.String())

    # Conjunction
    conjunction = db.Column(db.String())

    # Preposition
    preposition = db.Column(db.String())
    accusative = db.Column(db.Boolean())
    dative = db.Column(db.Boolean())

    __mapper_args__ = {
        "polymorphic_identity": "word",
        "polymorphic_on": type
    }

    def __repr__(self):
        return "<%s>" % "".join(["%s: %s, " % (column, getattr(self, column)) for column in self.__table__.columns._data
                                 if getattr(self, column) is not None])[:-2]


class Noun(Word):
    form = NounForm

    __mapper_args__ = {
        "polymorphic_identity": "noun"
    }


class Verb(Word):
    form = VerbForm

    __mapper_args__ = {
        "polymorphic_identity": "verb"
    }


class Adjective(Word):
    form = AdjectiveForm

    __mapper_args__ = {
        "polymorphic_identity": "adjective"
    }


class Adverb(Word):
    form = AdverbForm

    __mapper_args__ = {
        "polymorphic_identity": "adverb"
    }


class Conjunction(Word):
    form = ConjunctionForm

    __mapper_args__ = {
        "polymorphic_identity": "conjunction"
    }


class Preposition(Word):
    form = PrepositionForm

    __mapper_args__ = {
        "polymorphic_identity": "preposition"
    }