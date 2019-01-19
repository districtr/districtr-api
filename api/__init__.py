from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .controllers import plans, users
from .models import db


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(plans, url_prefix="/plans")
    app.register_blueprint(users, url_prefix="/users")

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
