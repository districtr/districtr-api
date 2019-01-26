from unittest.mock import patch

from api.controllers.register import send_sign_in_email


def test_registration_sends_email(client):
    with patch("api.controllers.register.send_sign_in_email") as send_sign_in_email:
        response = client.post(
            "/register/",
            json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
        )

        assert response.status_code == 201
        assert send_sign_in_email.call_count == 1


def test_template_works(app):
    with app.app_context():
        expected_link = "https://districtr.org/signin?token=abcdefg123456789"
        with patch("api.controllers.register.send_email") as send_email:
            send_sign_in_email("max.hully@gmail.com", "abcdefg123456789")
            content = send_email.call_args[0][3]
            assert expected_link in content


def test_registration_works_with_empty_db(app_without_roles):
    with app_without_roles.app_context():
        client = app_without_roles.test_client()
        with patch("api.controllers.register.send_sign_in_email") as send_sign_in_email:
            response = client.post(
                "/register/",
                json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
            )

            assert response.status_code == 201
            assert send_sign_in_email.call_count == 1
