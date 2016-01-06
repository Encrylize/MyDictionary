from app import db
from app.models import User
from app.utils import get_or_create, get_redirect_target, is_safe_url
from tests.general import AppTestCase


class TestUtils(AppTestCase):
    def test_get_or_create(self):
        user1, created1 = get_or_create(User, name='foo', social_id='bar')
        db.session.add(user1)
        db.session.commit()
        user2, created2 = get_or_create(User, name='foo', social_id='bar')
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(user1, user2)

    def test_is_safe_url(self):
        with self.app.test_request_context():
            self.assertFalse(is_safe_url('http://externalsite.com'))
            self.assertTrue(is_safe_url('http://' + self.app.config['SERVER_NAME']))
            self.assertTrue(is_safe_url('safe_internal_link'))

    def test_get_redirect_target(self):
        with self.app.test_request_context('/?next=http://externalsite.com'):
            self.assertIsNone(get_redirect_target())

        with self.app.test_request_context('/?next=safe_internal_link'):
            self.assertEquals(get_redirect_target(), 'safe_internal_link')
