from werkzeug.routing import ValidationError

from app.converters import WordClassConverter
from app.models import Noun, Verb
from tests.general import AppTestCase


class TestConverters(AppTestCase):
    def test_word_class_converter(self):
        word_class_converter = WordClassConverter(None)
        self.assertEquals(word_class_converter.to_python('noun'), Noun)
        self.assertEquals(word_class_converter.to_python('verb'), Verb)
        self.assertRaises(ValidationError, word_class_converter.to_python, 'invalid_word_class')
