from api.auth import create_signin_token
from api.models import User


def test_authenticated_user_can_create_new_token(client, user_headers):
    response = client.post("/tokens/", headers=user_headers)
    assert response.status_code == 201
    assert "token" in response.get_json()


def test_can_create_new_bearer_token_with_signin_token(app, client):
    with app.app_context():
        user = User.query.get(1)
        signin_token = create_signin_token(user).decode("utf-8")
        response = client.post("/tokens/", json={"token": signin_token})
    assert response.status_code == 201
    assert "token" in response.get_json()
