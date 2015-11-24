import unittest

from werkzeug.routing import ValidationError

from app import create_app, db
from app.converters import WordClassConverter
from app.models import Noun, Verb


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_word_class_converter(self):
        word_class_converter = WordClassConverter(None)
        self.assertEquals(word_class_converter.to_python('noun'), Noun)
        self.assertEquals(word_class_converter.to_python('verb'), Verb)
        self.assertRaises(ValidationError, word_class_converter.to_python,
                          'invalid_word_class')
