
from flask import Flask

from .models import db
from .controllers import PlansController
from .controllers import UsersController


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(PlansController, url_prefix="/plans")
    app.register_blueprint(UsersController, url_prefix="/users")

    db.create_all(app=app)

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
