from werkzeug.routing import ValidationError, UnicodeConverter
from sqlalchemy_utils import get_class_by_table

from app.models import Word


class WordClassConverter(UnicodeConverter):
    """ Converts a word class string into a class. """
    def to_python(self, value):
        try:
            word_class = get_class_by_table(Word, Word.__table__, data={"type": value})
            return word_class
        except ValueError:
            raise ValidationError()
