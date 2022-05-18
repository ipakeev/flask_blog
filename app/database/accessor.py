from sqlalchemy.dialects.postgresql import insert

from app.base import db
from app.database.models import User, Comment
from app.utils import encrypt_password


def init_admin(username: str, password: str):
    password = encrypt_password(password)
    stmt = insert(User) \
        .values(username=username, password=password, is_admin=True) \
        .on_conflict_do_update(index_elements=[User.username],
                               set_=dict(password=password, is_admin=True))
    db.session.execute(stmt)
    db.session.commit()


def add_user(username: str, password: str, is_admin=False) -> User:
    user = User(username, password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user


def add_comment(user_id: int, post_id: int, text: str) -> Comment:
    comment = Comment(user_id, post_id, text)
    db.session.add(comment)
    db.session.commit()
    return comment
