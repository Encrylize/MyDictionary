import unittest
from werkzeug.routing import ValidationError
from flask import g

from app import create_app, db
from app.models import User, Word, Noun, Verb
from app.converters import WordClassConverter, WordConverter


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_word_class_converter(self):
        word_class_converter = WordClassConverter(None)
        self.assertEquals(word_class_converter.to_python("noun"), Noun)
        self.assertEquals(word_class_converter.to_python("verb"), Verb)
        self.assertRaises(ValidationError, word_class_converter.to_python, "invalid_word_class")

    def test_word_converter(self):
        word_converter = WordConverter(None)

        # Add two users
        user1 = User(name="foo", social_id="bar")
        user2 = User(name="foo", social_id="baz")
        db.session.add(user1)
        db.session.add(user2)
        # Make user1 the current user
        g.user = user1

        # Add two words, one for each users dictionary
        word1 = Word(meaning="foo", examples="bar", dictionary=user1.dictionary)
        word2 = Word(meaning="foo", examples="bar", dictionary=user2.dictionary)
        db.session.add(word1)
        db.session.add(word2)
        db.session.commit()

        self.assertIsInstance(word_converter.to_python(word1.id), Word) # Test existing word belonging to the current user
        self.assertRaises(ValidationError, word_converter.to_python, 10) # Test non-existent word
        self.assertRaises(ValidationError, word_converter.to_python, word2.id) # Test ownership