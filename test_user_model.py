"""User model tests."""

import os
from unittest import TestCase
from models import db, User, Message, Follows
from app import app

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

class UserModelTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        """Create the test and add sample data."""
        # Drop all tables and recreate them for a clean slate
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        # Create the two users
        self.user1 = User.signup("user1", "user1@test.com", "password", None)
        self.user2 = User.signup("user2", "user2@test.com", "password", None)
        
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        # Lots of hanging was happening, so I added this to rollback any changes
        db.session.rollback()

    def test_repr(self):
        """Does the __repr__ method work?"""
        self.assertEqual(repr(self.user1), f"<User #{self.user1.id}: user1, user1@test.com>")

    def test_is_following(self):
        """Does is_following know when user1 is following user2?"""
        self.user1.following.append(self.user2)
        db.session.commit()
        self.assertTrue(self.user1.is_following(self.user2))

    def test_is_followed_by(self):
        """Does is_followed_by know when user2 is followed by user1?"""
        self.user1.following.append(self.user2)
        db.session.commit()
        self.assertTrue(self.user2.is_followed_by(self.user1))

    def test_user_create(self):
        """Does User.create work given valid info?"""
        user = User.signup("new_user", "newuser@test.com", "password", None)
        db.session.commit()
        self.assertIsNotNone(User.query.get(user.id))

    def test_user_authenticate(self):
        """Does User.authenticate work with good info?"""
        user = User.authenticate("user1", "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "user1")

    def test_user_authenticate_invalid(self):
        """Does User.authenticate work with wrong info?"""
        self.assertFalse(User.authenticate("user1", "wrongpassword"))
        self.assertFalse(User.authenticate("wronguser", "password"))
