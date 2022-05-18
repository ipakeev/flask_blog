from datetime import datetime

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from app.base import db
from app.utils import encrypt_password


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    is_admin = sa.Column(sa.Boolean, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    posts = relationship("Post")
    comments = relationship("Comment")

    def __init__(self, username: str, password: str, is_admin=False):
        self.username = username
        self.password = encrypt_password(password)
        self.is_admin = is_admin

    def get_id(self) -> str:
        return str(self.id)

    def is_correct_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username!r}, " \
               f"is_admin={self.is_admin}, created_at={self.created_at})"


class Post(db.Model):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    title = sa.Column(sa.String, nullable=False, unique=True)
    preview_image = sa.Column(sa.String)
    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    comments = relationship("Comment")

    def __init__(self, user_id: int, title: str, preview_image: str, text: str):
        self.user_id = user_id
        self.title = title
        self.preview_image = preview_image
        self.text = text

    def __repr__(self):
        return f"Post(id={self.id}, user_id={self.user_id}, title={self.title!r}, " \
               f"created_at={self.created_at})"


class Comment(db.Model):
    __tablename__ = "comments"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    post_id = sa.Column(sa.ForeignKey(Post.id, ondelete="CASCADE"), nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, user_id: int, post_id: int, text: str):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text

    def __repr__(self):
        return f"Comment(id={self.id}, user_id={self.user_id}, post_id={self.post_id}, " \
               f"text={self.text!r}, created_at={self.created_at})"
