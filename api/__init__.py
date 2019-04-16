from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .controllers import register_blueprints
from .exceptions import register_error_handlers
from .models import db
from .result import ApiResult
from .commands import admin_cli


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

    if app.config.get("SENTRY_DSN") is not None:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(dsn=app.config["SENTRY_DSN"], integrations=[FlaskIntegration()])

    db.init_app(app)
    Migrate(app, db)

    register_blueprints(app)
    register_error_handlers(app)

    @app.route("/")
    def hello():
        return "Hello, universe!"

    app.cli.add_command(admin_cli)

    return app
