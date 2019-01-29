from unittest.mock import patch

from api.controllers.register import send_registration_email, send_signin_email


def test_registration_sends_email(client):
    with patch(
        "api.controllers.register.send_registration_email"
    ) as send_registration_email:
        response = client.post(
            "/register/",
            json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
        )

        assert response.status_code == 201
        assert send_registration_email.call_count == 1


def test_templates_work(app):
    with app.app_context():
        expected_link = app.config["FRONTEND_BASE_URL"] + "/?token=abcdefg123456789"
        with patch("api.controllers.register.send_email") as send_email:
            send_signin_email("max.hully@gmail.com", b"abcdefg123456789")
            content = send_email.call_args[0][3]
            assert expected_link in content

            send_registration_email("max.hully@gmail.com", b"abcdefg123456789")
            content = send_email.call_args[0][3]
            assert expected_link in content


def test_registration_works_with_empty_db(app_without_roles):
    with app_without_roles.app_context():
        client = app_without_roles.test_client()
        with patch(
            "api.controllers.register.send_registration_email"
        ) as send_registration_email:
            response = client.post(
                "/register/",
                json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
            )

            assert response.status_code == 201
            assert send_registration_email.call_count == 1


def test_does_not_fail_when_SEND_EMAILS_is_missing_from_config(app_without_roles):
    with app_without_roles.app_context():
        del app_without_roles.config["SEND_EMAILS"]
        client = app_without_roles.test_client()
        with patch(
            "api.controllers.register.send_registration_email"
        ) as send_registration_email:
            response = client.post(
                "/register/",
                json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
            )

            assert response.status_code == 201
            assert send_registration_email.call_count == 1


def test_signin(client, user_record):
    with patch("api.controllers.register.send_signin_email") as send_signin_email:
        response = client.post("/signin/", json={"email": user_record["email"]})

        assert response.status_code == 201
        assert send_signin_email.call_count == 1


def test_registration_of_existing_user_sends_signin_email(client, user_record):
    with patch("api.controllers.register.send_signin_email") as send_signin_email:
        response = client.post(
            "/register/",
            json={
                "first": user_record["first"],
                "last": user_record["last"],
                "email": user_record["email"],
            },
        )

        assert response.status_code == 201
        assert "already exists" in response.get_json()["message"]
        assert send_signin_email.call_count == 1
