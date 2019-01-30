from api.schemas import PlaceRequestSchema


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
            },
        },
    )
    assert response.status_code == 201


def test_can_list_requests_with_admin_auth(client, admin_headers):
    payload = {
        "name": "Alabama",
        "information": "",
        "districtTypes": "State senate",
        "user": {"first": "New", "last": "Person", "email": "someone.else@example.com"},
    }
    client.post("/requests/", json=payload)
    response = client.get("/requests/", headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "Alabama"


def test_schema_validates_a_good_request():
    schema = PlaceRequestSchema()
    schema.load(
        {
            "name": "Alabama",
            "information": "",
            "districtTypes": "State senate",
            "user": {
                "first": "New",
                "last": "Person",
                "email": "someone.else@example.com",
            },
        }
    )
