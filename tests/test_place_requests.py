from unittest.mock import patch

import pytest
from marshmallow import ValidationError

from api.schemas import PlaceRequestSchema


@pytest.fixture
def good_request():
    return {
        "name": "Alabama",
        "information": "We need to district it",
        "districtTypes": "State senate",
        "user": {
            "first": "New",
            "last": "Person",
            "email": "someone.else@example.com",
            "organization": "MGGG",
        },
    }


def test_can_create_requests_with_existing_user(client):
    response = client.post(
        "/requests/",
        json={
            "name": "Alabama",
            "information": "",
            "districtTypes": "State senate",
            "user": {"first": "Example", "last": "Person", "email": "me@example.com"},
        },
    )
    assert response.status_code == 201


def test_can_create_requests_with_new_user(client):
    response = client.post(
        "/requests/",
        json={
            "name": "Alabama",
            "information": "",
            "districtTypes": "State senate",
            "user": {
                "first": "New",
                "last": "Person",
                "email": "someone.else@example.com",
                "organization": "MGGG",
            },
        },
    )
    assert response.status_code == 201


def test_can_list_requests_with_admin_auth(client, admin_headers, good_request):
    client.post("/requests/", json=good_request)

    response = client.get("/requests/", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()[0]["name"] == good_request["name"]


def test_schema_validates_a_good_request(good_request):
    schema = PlaceRequestSchema()
    schema.load(good_request)


def test_schema_invalidates_a_bad_request():
    schema = PlaceRequestSchema()
    with pytest.raises(ValidationError):
        schema.load(
            {
                "information": "",
                "user": {
                    "first": "New",
                    "last": "Person",
                    "email": "someone.else@example.com",
                },
            }
        )


def test_sends_an_email(client, good_request):
    with patch("api.controllers.requests.send_email") as send_email:
        client.post("/requests/", json=good_request)
        content = send_email.call_args[0][3]
        assert good_request["information"] in content
