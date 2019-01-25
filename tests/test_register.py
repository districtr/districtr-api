from unittest.mock import patch


def test_registration_sends_email(client):
    with patch("api.controllers.register.send_sign_in_email") as send_sign_in_email:
        response = client.post(
            "/register/",
            json={"first": "Emmy", "last": "Noether", "email": "emmy@brynmawr.edu"},
        )

        assert response.status_code == 201
        assert send_sign_in_email.call_count == 1
