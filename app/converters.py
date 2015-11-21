from werkzeug.routing import ValidationError, UnicodeConverter, IntegerConverter
from sqlalchemy_utils import get_class_by_table
from flask import g

from app.models import Word


class WordClassConverter(UnicodeConverter):
    """ Converts a word class string into a class. """
    def to_python(self, value):
        try:
            word_class = get_class_by_table(Word, Word.__table__, data={"type": value})
            return word_class
        except ValueError:
            raise ValidationError()


class WordConverter(IntegerConverter):
    """ Converts a valid Word ID into a Word object. """
    def to_python(self, value):
        word = Word.query.get(value)
        if word is None or word.dictionary.creator != g.user:
            raise ValidationError()
        else:
            return word