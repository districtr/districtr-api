from api.models import User, db
from api.schemas.user import UserSchema


def test_can_list_users(client, admin_headers):
    response = client.get("/users/", headers=admin_headers)
    assert len(response.get_json()) >= 1


def test_list_users_requires_admin(client, user_headers):
    response = client.get("/users/")
    assert response.status_code == 401

    response = client.get("/users/", headers=user_headers)
    assert response.status_code == 403


def test_create_new_user(client, admin_headers):
    response = client.post(
        "/users/",
        json={
            "first": "User",
            "last": "Name",
            "email": "user@example.com",
            "roles": ["user", "admin"],
        },
        headers=admin_headers,
    )
    assert response.status_code == 201


def test_create_new_user_requires_admin_role(client):
    response = client.post(
        "/users/",
        json={
            "first": "User",
            "last": "Name",
            "email": "user@example.com",
            "roles": ["user", "admin"],
        },
    )
    assert 400 <= response.status_code < 500


def test_deleting_a_user_requires_admin_role(client, admin_headers):
    response = client.post(
        "/users/",
        json={
            "first": "User",
            "last": "Name",
            "email": "user@example.com",
            "roles": ["user", "admin"],
        },
        headers=admin_headers,
    )
    print(response)
    user_id = response.get_json()["id"]

    # Try to delete without auth headers
    assert client.delete("/users/{}".format(user_id)).status_code == 401

    # Can delete with admin auth headers
    deletion_response = client.delete(
        "/users/{}".format(user_id), headers=admin_headers
    )
    assert deletion_response.status_code == 204


def test_user_schema_has_user_role_by_default(app):
    with app.app_context():
        schema = UserSchema()

        user = schema.load(
            {"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"}
        )

    assert user["roles"] == [{"name": "user"}]


def test_emails_must_be_unique(client, admin_headers):
    response = client.post(
        "/users/",
        json={"first": "Mac", "last": "Sully", "email": "me@example.com"},
        headers=admin_headers,
    )

    assert response.status_code == 409


def test_can_add_role(app):
    with app.app_context():
        user = User.from_schema_load(
            dict(first="Example", last="Person", email="example123@example.com")
        )
        user.add_role("admin")
        db.session.add(user)
        db.session.commit()

        id = user.id
        retrieved_user = User.query.get(id)
        assert set(role.name for role in retrieved_user.roles) == {"user", "admin"}


def test_can_add_new_role(app_without_roles):
    app = app_without_roles
    with app.app_context():
        user = User.from_schema_load(
            dict(first="Example", last="Person", email="example123@example.com")
        )
        user.add_role("admin")
        db.session.add(user)
        db.session.commit()

        id = user.id
        retrieved_user = User.query.get(id)
        assert set(role.name for role in retrieved_user.roles) == {"user", "admin"}


def test_adding_a_role_is_idempotent(app_without_roles):
    app = app_without_roles
    with app.app_context():
        user = User.from_schema_load(
            dict(first="Example", last="Person", email="example123@example.com")
        )
        user.add_role("admin")
        db.session.add(user)
        db.session.commit()

        id = user.id
        retrieved_user = User.query.get(id)
        assert set(role.name for role in retrieved_user.roles) == {"user", "admin"}

        retrieved_user.add_role("admin")
        db.session.commit()

        id = user.id
        retrieved_user_again = User.query.get(id)
        assert set(role.name for role in retrieved_user_again.roles) == {
            "user",
            "admin",
        }


def test_can_add_a_role_to_existing_user(app_without_roles):
    app = app_without_roles
    with app.app_context():
        user = User.from_schema_load(
            dict(first="Example", last="Person", email="example123@example.com")
        )
        db.session.add(user)
        db.session.commit()

        id = user.id
        retrieved_user = User.query.get(id)
        assert set(role.name for role in retrieved_user.roles) == {"user"}

        retrieved_user.add_role("admin")
        db.session.commit()

        id = user.id
        retrieved_user_again = User.query.get(id)
        assert set(role.name for role in retrieved_user_again.roles) == {
            "user",
            "admin",
        }
