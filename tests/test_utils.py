import unittest

from app import create_app, db
from app.utils import get_or_create, is_safe_url, get_redirect_target
from app.models import User


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

    def test_get_or_create(self):
        user1, created1 = get_or_create(User, name="foo", social_id="bar")
        db.session.add(user1)
        db.session.commit()
        user2, created2 = get_or_create(User, name="foo", social_id="bar")
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(user1, user2)

    def test_is_safe_url(self):
        with self.app.test_request_context():
            self.assertFalse(is_safe_url("http://externalsite.com"))
            self.assertTrue(is_safe_url("http://" + self.app.config["SERVER_NAME"]))
            self.assertTrue(is_safe_url("safe_internal_link"))

    def test_get_redirect_target(self):
        with self.app.test_request_context("/?next=http://externalsite.com"):
            self.assertIsNone(get_redirect_target())

        with self.app.test_request_context("/?next=safe_internal_link"):
            self.assertEquals(get_redirect_target(), "safe_internal_link")