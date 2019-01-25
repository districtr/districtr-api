def test_can_list_users(client):
    response = client.get("/users/")
    assert len(response.get_json()) >= 1


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
    user_id = response.get_json()["id"]

    # Try to delete without auth headers
    assert client.delete("/users/{}".format(user_id)).status_code == 401

    # Can delete with admin auth headers
    deletion_response = client.delete(
        "/users/{}".format(user_id), headers=admin_headers
    )
    assert deletion_response.status_code == 204
