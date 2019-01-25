from flask import request

from api.auth import admin_only, authenticate, load_token_data


def test_get_user_from_request(app, admin_headers):
    with app.test_request_context("/", method="GET", headers=admin_headers):
        user_data = load_token_data(request)

    assert set(user_data["roles"]) == {"user", "admin"}


def test_authenticated_route_gives_401_when_no_token_provided(app):
    with app.app_context():

        @app.route("/test_route")
        @authenticate
        def route():
            return "OK"

    client = app.test_client()

    response = client.get("/test_route")
    assert response.status_code == 401


def test_admin_only_route_gives_403_with_scope_error_for_non_admin(app, user_headers):
    with app.app_context():

        @app.route("/test_route")
        @admin_only
        def route():
            return "OK"

    client = app.test_client()

    response = client.get("/test_route", headers=user_headers)
    assert response.status_code == 403
    assert "insufficient_scope" in response.headers["WWW-Authenticate"]


def test_admin_only_route_gives_401_with_no_info_if_no_token_provided(app):
    with app.app_context():

        @app.route("/test_route")
        @admin_only
        def route():
            return "OK"

    client = app.test_client()

    response = client.get("/test_route")
    assert response.status_code == 401
    assert "error" not in response.headers["WWW-Authenticate"]
