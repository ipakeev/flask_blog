from flask import Flask

from app.base import init_db, login_manager
from app.database.models import User
from app.web.blueprint.admin import admin_app
from app.web.blueprint.main_app import main_app
from app.web.config import Config


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.filter_by(id=int(user_id)).first()


def create_app(config: Config) -> Flask:
    app = Flask("main")
    app.config["ENV"] = "development"
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI

    app.register_blueprint(main_app, url_prefix="/")
    app.register_blueprint(admin_app, url_prefix="/admin")

    init_db(app)
    login_manager.init_app(app)

    return app
