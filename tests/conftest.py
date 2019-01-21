import pytest

from api import create_app
from api.auth import create_bearer_token
from api.models import Role, User, db
from api.schemas import PlanSchema


@pytest.fixture
def app(user, plan_record):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": b"my_secret_key",
        }
    )

    with app.app_context():
        db.create_all()

        admin_role = Role(name="admin")
        user_role = Role(name="user")
        db.session.add(admin_role)
        db.session.add(user_role)

        user.roles = [admin_role, user_role]

        db.session.add(user)

        plan = PlanSchema().load(plan_record)
        plan.user = user
        db.session.add(plan)

        db.session.commit()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_record():
    return {"first": "Max", "last": "Hully", "email": "max.hully@gmail.com"}


@pytest.fixture
def user(user_record):
    return User(**user_record)


@pytest.fixture
def plan_record():
    return {"name": "My plan", "mapping": {"1": 0}}


@pytest.fixture
def token(app):
    with app.app_context():
        return create_bearer_token(User.query.get(1))


@pytest.fixture
def auth_headers(token):
    return {"Authorization": b"Bearer " + token}
