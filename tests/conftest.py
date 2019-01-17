import pytest

from api import create_app
from api.models import db


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_with_user(client):
    client.post(
        "/users/",
        json={"first": "Max", "last": "Hully", "email": "max.hully@gmail.com"},
    )
    return client
