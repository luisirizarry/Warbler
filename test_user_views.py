"""User View tests."""

import os
from unittest import TestCase
from models import db, User
from app import app, CURR_USER_KEY

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

# disable the csrf token
app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        
        self.client = app.test_client()

        self.testuser = User.signup(username="testuser", email="test@test.com", password="password", image_url=None)
        db.session.commit()

    def test_following_page_logged_in(self):
        """Can a logged-in user view their following page?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp.status_code, 200)

    def test_following_page_logged_out(self):
        """Is a logged-out user not allowed to view the following page?"""
        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}/following", follow_redirects=True)
            self.assertIn("Access unauthorized", str(resp.data))

    def test_edit_profile(self):
        """Can logged-in user edit profile?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/profile", data={"username": "newusername", "password": "password"}, follow_redirects=True)
            self.assertIn("newusername", str(resp.data))
