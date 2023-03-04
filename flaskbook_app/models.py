from sqlalchemy.orm import backref
from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    posts_made = db.relationship('Post', backref='author', lazy=True, foreign_keys='Post.author_id')
    posts_received = db.relationship('Post', back_populates='recipient', lazy=True, foreign_keys='Post.recipient_id')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # author = db.relationship('User', back_populates='posts_made', foreign_keys=[author_id])
    # recipient = db.relationship('User', back_populates='posts_received', foreign_keys=[recipient_id])

    def __repr__(self):
        return f"Post('{self.content}', '{self.created_at}')"


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


    def __repr__(self):
        return f"Interest('{self.name}', '{self.description}')"

class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f"Follow('{self.follower_id}', '{self.followed_id}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"
