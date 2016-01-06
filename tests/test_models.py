from app import db
from app.models import User
from tests.general import AppTestCase


class TestModels(AppTestCase):
    def test_user_initialization(self):
        user = User(name='foo', social_id='bar')
        db.session.add(user)
        db.session.commit()
        dictionary = user.dictionary

        self.assertIsNotNone(user)
        self.assertIsNotNone(dictionary)
