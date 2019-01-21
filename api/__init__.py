from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .controllers import plans, users
from .exceptions import ApiException
from .models import db
from .result import ApiResult


class ApiFlask(Flask):
    def make_response(self, result):
        if isinstance(result, ApiResult):
            return result.to_response()
        return Flask.make_response(self, result)


def create_app(test_config=None):
    app = ApiFlask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(plans, url_prefix="/plans")
    app.register_blueprint(users, url_prefix="/users")

    app.register_error_handler(ApiException, lambda err: err.to_result())

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
