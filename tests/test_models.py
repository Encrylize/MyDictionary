import unittest

from app import create_app, db
from app.models import User


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

    def test_user_initialization(self):
        user = User(name='foo', social_id='bar')
        db.session.add(user)
        db.session.commit()
        dictionary = user.dictionary

        self.assertIsNotNone(user)
        self.assertIsNotNone(dictionary)
