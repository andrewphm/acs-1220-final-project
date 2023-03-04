
# import app
import unittest
from datetime import datetime
from flaskbook_app.extensions import app, db
from flaskbook_app.models import User, Post, Comment, Follow

class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.user1 = User(username='user1', password_hash='password1', created_at=datetime.utcnow())
        self.user2 = User(username='user2', password_hash='password2', created_at=datetime.utcnow())
        self.post1 = Post(content='Test post 1', created_at=datetime.utcnow(), author_id=self.user1.id, recipient_id=self.user1.id)
        self.post2 = Post(content='Test post 2', created_at=datetime.utcnow(), author_id=self.user1.id, recipient_id=self.user2.id)
        # self.follow1 = Follow(follower_id=self.user1.id, followed_id=self.user2.id)
        self.comment1 = Comment(body='Test comment 1', timestamp=datetime.utcnow(), user_id=self.user1.id, post_id=self.post1.id)

        db.session.add_all([self.user1, self.user2, self.post1, self.post2, self.comment1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_model(self):
      # Check that the user model was saved to the database
      self.assertEqual(User.query.count(), 2)

      # Check that the user model fields match the values that were saved
      self.assertEqual(self.user1.username, 'user1')
      self.assertEqual(self.user1.password_hash, 'password1')
      self.assertEqual(self.user1.created_at, self.user1.created_at)

if __name__ == '__main__':
    unittest.main()
