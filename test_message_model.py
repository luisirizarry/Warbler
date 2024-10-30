"""Message model tests."""

import os
from unittest import TestCase
from models import db, User, Message
from app import app

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

class MessageModelTestCase(TestCase):
    """Test Message model."""

    def setUp(self):
        """Create test client and add sample data."""
        # Drop all tables and recreate them for a clean slate
        db.drop_all()
        db.create_all()

        # Set up a test client
        self.client = app.test_client()

        # Create a test user
        self.user = User.signup("testuser", "testmessenger@test.com", "password", None)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic Message model work?"""
        msg = Message(text="Im the best coder!!", user_id=self.user.id)
        db.session.add(msg)
        db.session.commit()

        # Message should have the same text and be from the same user
        self.assertEqual(msg.text, "Im the best coder!!")
        self.assertEqual(msg.user_id, self.user.id)

    def test_is_liked_by(self):
        """Can we correctly detect if a message is liked by a user?"""
        msg = Message(text="No im the best coder", user_id=self.user.id)
        db.session.add(msg)
        db.session.commit()
        self.user.likes.append(msg)
        db.session.commit()

        self.assertTrue(msg.is_liked_by(self.user))
