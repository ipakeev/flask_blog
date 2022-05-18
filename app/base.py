from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def init_db(app: Flask):
    import app.database.models as m1
    _ = m1  # to avoid deleting imported module by the Pycharm

    db.init_app(app)
    db.create_all(app=app)
