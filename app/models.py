from collections import OrderedDict

from flask_login import UserMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils import TSVectorType

from app import db
from app.forms import (AdjectiveForm, AdverbForm, ConjunctionForm, NounForm,
                       PrepositionForm, VerbForm, WordForm)

make_searchable()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    dictionary = db.relationship('Dictionary',
                                 uselist=False,
                                 backref='creator',
                                 cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        """ Initializes the user and creates their dictionary. """
        super().__init__(**kwargs)
        self.dictionary = Dictionary(creator=self)

    def __repr__(self):
        return '<User %d>' % self.id


class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    words = db.relationship('Word',
                            lazy='dynamic',
                            backref='dictionary',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return '<Dictionary %d>' % self.id


class WordQuery(BaseQuery, SearchQueryMixin):
    pass


class Word(db.Model):
    # General
    query_class = WordQuery
    search_vector = db.Column(TSVectorType(
        'singular', 'plural', 'infinitive', 'past_tense',
        'present_perfect_tense', 'positive', 'comparative', 'superlative',
        'adverb', 'conjunction', 'preposition', 'meaning', 'examples'))

    id = db.Column(db.Integer, primary_key=True)
    form = WordForm
    meaning = db.Column(db.String())
    examples = db.Column(db.String())
    type = db.Column(db.String())
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionary.id'))

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

    __mapper_args__ = {'polymorphic_identity': 'word', 'polymorphic_on': type}

    @property
    def header(self):
        return ''

    @property
    def subheader(self):
        return '%s. %s' % (self.type, self.meaning)

    @property
    def body(self):
        return {}

    @property
    def footer(self):
        return self.examples

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<%s %d>' % (self.type.capitalize(), self.id)


class Noun(Word):
    form = NounForm

    __mapper_args__ = {'polymorphic_identity': 'noun'}

    @property
    def header(self):
        return self.singular

    @property
    def subheader(self):
        return '%s, %s. %s' % (self.type, self.gender, self.meaning)

    @property
    def body(self):
        return OrderedDict(
            (
                ('Singular', self.singular),
                ('Plural', self.plural)
            )
        )


class Verb(Word):
    form = VerbForm

    __mapper_args__ = {'polymorphic_identity': 'verb'}

    @property
    def header(self):
        return self.infinitive

    @property
    def subheader(self):
        return '%s, consonant change in 2nd/3rd person, singular. %s' % (
            self.type, self.meaning) if self.consonant_change else '%s. %s' % (
                self.type, self.meaning)

    @property
    def body(self):
        return OrderedDict(
            (
                ('Infinitive', self.infinitive),
                ('Past tense', self.past_tense),
                ('Present perfect tense', self.present_perfect_tense)
            )
        )


class Adjective(Word):
    form = AdjectiveForm

    __mapper_args__ = {'polymorphic_identity': 'adjective'}

    @property
    def header(self):
        return self.positive

    @property
    def body(self):
        return OrderedDict(
            (
                ('Positive', self.positive),
                ('Comparative', self.comparative),
                ('Superlative', self.superlative)
            )
        )


class Adverb(Word):
    form = AdverbForm

    __mapper_args__ = {'polymorphic_identity': 'adverb'}

    @property
    def header(self):
        return self.adverb


class Conjunction(Word):
    form = ConjunctionForm

    __mapper_args__ = {'polymorphic_identity': 'conjunction'}

    @property
    def header(self):
        return self.conjunction


class Preposition(Word):
    form = PrepositionForm

    __mapper_args__ = {'polymorphic_identity': 'preposition'}

    @property
    def header(self):
        return self.preposition

    @property
    def subheader(self):
        if self.accusative and self.dative:
            return '%s, accusative/dative. %s' % (self.type, self.meaning)
        elif self.accusative:
            return '%s, accusative. %s' % (self.type, self.meaning)
        elif self.dative:
            return '%s, dative. %s' % (self.type, self.meaning)
        else:
            return super().subheader
