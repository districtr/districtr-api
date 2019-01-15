
from flask import Flask
from flask_cors import CORS

from .models import db


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    from .controllers import PlansController
    from .controllers import UsersController
    
    app.register_blueprint(PlansController, url_prefix="/plans")
    app.register_blueprint(UsersController, url_prefix="/users")

    db.create_all(app=app)

    @app.route("/")
    def hello():
        return "Hello, world!"

    return app
