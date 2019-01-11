from flask import Flask

from .controllers import plans, users
from .models import db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(plans, url_prefix="/plans")
    app.register_blueprint(users, url_prefix="/users")

    db.create_all(app=app)

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
