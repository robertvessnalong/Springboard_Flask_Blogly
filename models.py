"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime


db = SQLAlchemy()

default_image = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'
        
    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_image)

    @property
    def full_name(self):
        """ Return Full Name """

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(180), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=backref("user", cascade="all,delete"))

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at} {self.user_id}"


class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)




class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')

