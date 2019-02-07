import pytest

from api import create_app
from api.auth import create_bearer_token
from api.models import Place, Role, User, db
from api.schemas import PlanSchema

test_config = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECRET_KEY": b"my_secret_key",
    "SEND_EMAILS": False,
    "FRONTEND_BASE_URL": "https://districtr.org",
}


@pytest.fixture
def app_without_roles(user, plan_record):
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def app(user, plan_record):
    app = create_app(test_config)

    with app.app_context():
        db.create_all()

        admin_role = Role(name="admin")
        user_role = Role(name="user")
        db.session.add(admin_role)
        db.session.add(user_role)

        # Admin user
        user.roles = [admin_role, user_role]
        db.session.add(user)

        # Non-admin user
        non_admin = User(first="Example", last="Person", email="person@example.com")
        non_admin.roles = [user_role]
        db.session.add(non_admin)

        place = Place(name="Lowell, MA", description="A town")
        db.session.add(place)

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
    return {
        "first": "Example",
        "last": "Person",
        "email": "me@example.com",
        "roles": ["user", "admin"],
    }


@pytest.fixture
def user(user_record):
    return User(
        first=user_record["first"], last=user_record["last"], email=user_record["email"]
    )


@pytest.fixture
def plan_record():
    return {"name": "My plan", "mapping": {"1": 0}, "place_id": 1}


@pytest.fixture
def token(app):
    with app.app_context():
        return create_bearer_token(User.query.get(1))


@pytest.fixture
def admin_headers(token):
    return {"Authorization": b"Bearer " + token}


@pytest.fixture
def user_token(app):
    with app.app_context():
        return create_bearer_token(User.query.get(2))


@pytest.fixture
def user_headers(user_token):
    return {"Authorization": b"Bearer " + user_token}


@pytest.fixture
def place_record_with_elections():
    return {
        "name": "Alabama",
        "description": "A state",
        "elections": [
            {
                "race": "Presidential",
                "year": 2008,
                "voteTotals": [
                    {"key": "2008D", "name": "Democratic"},
                    {"key": "2008R", "name": "Republican"},
                ],
            }
        ],
    }


@pytest.fixture
def place_record_with_tilesets():
    return {
        "name": "Alabama",
        "description": "A state",
        "tilesets": [
            {
                "type": "fill",
                "source": {"type": "vector", "url": "mapbox://districtr.pa_vtds"},
                "sourceLayer": "pa_vtds",
            },
            {
                "type": "circle",
                "source": {
                    "type": "vector",
                    "url": "mapbox://districtr.pa_vtds_points",
                },
                "sourceLayer": "pa_vtds_points",
            },
        ],
    }
