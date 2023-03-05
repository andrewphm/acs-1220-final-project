from sqlalchemy.orm import backref
from flask_login import UserMixin
from .extensions import db
from datetime import datetime


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Follow('{self.follower_id}', '{self.followed_id}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_interests = db.relationship('UserInterest', backref='user', lazy=True)
    avatar = db.Column(db.String(255), default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref='follower',
        lazy='dynamic',
    )
    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref='followed',
        lazy='dynamic',
    )

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)

    def unfollow(self, user):
        follow = self.followed.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    photo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts', lazy=True, foreign_keys=[author_id])
    receiver = db.relationship('User', backref='receieved_posts', lazy=True, foreign_keys=[receiver_id])

    def __repr__(self):
        return f"Post('{self.content}', '{self.created_at}')"


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    # Define a many-to-many relationship between Interest and UserInterest
    user_interests = db.relationship('UserInterest', backref='interest', lazy=True)

    def __repr__(self):
        return f"Interest('{self.name}')"

class UserInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), nullable=False)




# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

#     def __repr__(self):
#         return f"Comment('{self.body}', '{self.timestamp}')"
