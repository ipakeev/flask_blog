# set SECRET_KEY="adsdfjalskdjgaldjg;laeijg"
# set DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/test
import os

from app.database.accessor import init_admin
from app.web.app import create_app
from app.web.config import Config

if __name__ == '__main__':
    config = Config(
        SECRET_KEY=os.environ["SECRET_KEY"],
        DATABASE_URI=os.environ["DATABASE_URI"]
    )

    app = create_app(config)
    with app.app_context():
        init_admin("admin", "admin")
    app.run(host="0.0.0.0", debug=True)
