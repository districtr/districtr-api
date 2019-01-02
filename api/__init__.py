from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db

    db.init_app(app)

    from .plan import bp

    app.register_blueprint(bp, url_prefix="/plans")

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
